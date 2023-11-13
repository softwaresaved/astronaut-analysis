#!/bin/bash
# SPDX-FileCopyrightText: 2018 German Aerospace Center (DLR)
# SPDX-License-Identifier: MIT


# Exit when any command fails
set -e

# Install required dependencies
pip install -r requirements.txt
echo "Successfully installed required packages"

# Check the code using the flake8 linter
flake8 --max-line-length 120 astronaut-analysis.py

# Check that copyright and license information for all files is available
reuse --root ../ lint

# Check that the script is basically working and creating the same results
python astronaut-analysis.py
test -f boxplot.png
test -f combined_histogram.png
test -f female_humans_in_space.png
test -f humans_in_space.png
test -f male_humans_in_space.png
echo "Successfully created the plots"
