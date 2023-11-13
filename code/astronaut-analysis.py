"""
SPDX-FileCopyrightText: 2018 German Aerospace Center (DLR)
SPDX-License-Identifier: MIT


This script analysis the astronaut data set and creates different plots as result.
"""


from datetime import date

import pandas as pd
import matplotlib.pyplot as plt


_ASTRONAUT_DATA_FILE = "../data/astronauts.json"


##
# Data preparation functions
##
def prepare_data_set(df):
    df = rename_columns(df)
    df = df.set_index("astronaut_id")

    # Set pandas dtypes for columns with date or time
    df = df.dropna(subset=["time_in_space"])
    df["time_in_space"] = df["time_in_space"].astype(int)
    df["time_in_space"] = pd.to_timedelta(df["time_in_space"], unit="m")
    df["birthdate"] = pd.to_datetime(df["birthdate"])
    df["date_of_death"] = pd.to_datetime(df["date_of_death"])
    df.sort_values("birthdate", inplace=True)

    # Calculate extra columns from the original data
    df["time_in_space_D"] = df["time_in_space"].astype("timedelta64[D]")
    df["alive"] = df["date_of_death"].apply(is_alive)
    df["age"] = df["birthdate"].apply(calculate_age)
    df["died_with_age"] = df.apply(died_with_age, axis=1)
    return df


def rename_columns(df):
    """
    The original column naming in the data set is not useful
    for programming with pandas. So we rename it.
    """

    name_mapping = {
        "astronaut": "astronaut_id",
        "astronautLabel": "name",
        "birthplaceLabel": "birthplace",
        "sex_or_genderLabel": "sex_or_gender",
    }
    df = df.rename(index=str, columns=name_mapping)
    return df


def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def is_alive(date_of_death):
    if pd.isnull(date_of_death):
        return True
    return False


def died_with_age(row):
    if pd.isnull(row["date_of_death"]):
        return None
    born = row["birthdate"]
    today = row["date_of_death"]
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


##
# Plot functions
##
def create_time_of_x_in_space(df, filename, title):
    """
    This function generated a plot with the summed up time of 'living beings'
    in space over the years by their birthday's.
    """

    reduced_df = df[["birthdate", "time_in_space", "time_in_space_D"]].copy()
    reduced_df["accumulated_time_in_minutes"] = reduced_df["time_in_space"].cumsum()
    reduced_df["accumulated_time_in_days"] = reduced_df["time_in_space_D"].cumsum()
    axs = reduced_df.plot(x="birthdate", y="accumulated_time_in_days")
    axs.set_title(title)
    axs.set_xlabel("Years ")
    axs.set_ylabel("t in days")
    save(axs.get_figure(), filename)


def create_age_histogram(age_df, died_df):
    """
    The function generates a combined histogram of astronauts
    in the categories 'age at dead' and 'age alive'.
    """

    fig, axs = plt.subplots(1, 1)
    axs.hist(
        [died_df["died_with_age"], age_df["age"]],
        bins=70,
        range=(31, 100),
        stacked=True,
    )
    axs.set_xlabel("Age")
    axs.set_ylabel("Number of astronauts")
    axs.set_title("Dead vs. Alive astronauts")
    save(fig, "combined_histogram.png")


def create_age_boxplot(age_df, died_df):
    """
    The function generates a box plot of astronauts age distribution
    in the categories dead and alive.
    """

    fig, axs = plt.subplots(1, 1)
    axs.boxplot([died_df["died_with_age"], age_df["age"]])
    axs.set_title("Age distribution; Dead vs. Alive astronauts")
    axs.set_xlabel("Category")
    plt.setp(axs, xticks=[1, 2], xticklabels=["Dead", "Alive"])
    axs.set_ylabel("Age")
    save(fig, "boxplot.png")


def save(fig, filename):
    fig.savefig(filename)


def perform_analysis():
    """Glues data preparation and plotting."""

    # Set up directory structure and preprocess data
    df = pd.read_json(_ASTRONAUT_DATA_FILE)
    df = prepare_data_set(df)

    # Creat plots
    plt.style.use("ggplot")

    # Male humans in space
    df_male = df.loc[
        df["sex_or_gender"] == "male", ["birthdate", "time_in_space", "time_in_space_D"]
    ].copy()
    create_time_of_x_in_space(
        df_male,
        "male_humans_in_space.png",
        "Total time male humans have spend in space",
    )

    # Female humans in space
    df_female = df.loc[
        df["sex_or_gender"] == "female",
        ["birthdate", "time_in_space", "time_in_space_D"],
    ].copy()
    create_time_of_x_in_space(
        df_female,
        "female_humans_in_space.png",
        "Total time female humans have spend in space",
    )

    # Humans in space
    create_time_of_x_in_space(
        df, "humans_in_space.png", "Total time humans have spend in space"
    )

    # Dead and alive astronauts analysis
    died_df = df.loc[df["alive"] == 0, ["died_with_age"]].copy()
    age_df = df.loc[df["alive"] == 1, ["age"]].copy()

    # Combined histogram of dead and alive astronauts
    create_age_histogram(age_df, died_df)

    # Box plots of dead vs alive astronauts
    create_age_boxplot(age_df, died_df)


# Main entry point
if __name__ == "__main__":
    perform_analysis()
