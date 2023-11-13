<!--
SPDX-FileCopyrightText: 2018 German Aerospace Center (DLR)
SPDX-License-Identifier: CC-BY-4.0
-->

# General Information

Please note that this **is not** a usual Git repository.
It's main purpose is to demonstrate every important step performed in a workshop.
Consequently, branches are treated differently:
- Every branch except the default branch `master` shows the final results of a specific step.
- The default branch adds further documentation and automates checking some details.

To maintain the repository structure contributions must follow a process.  

## External Contributions 

1. **Create a fork** from this repository.
  - Integrate your contributions to the branch `master`.
1. **Create Merge Request**.
  - Request to merge into `master`.
  - Provide information about your change.

We will integrate your changes manually and close the merge request.
In addition, we add your name to the [list of contributors](https://gitlab.com/hifis/hifis-workshops/make-your-code-ready-for-publication/workshop-materials#contributors).

## Internal Contributions

This section explains how to integrate external and own contributions as a project developer or maintainer.

### Changes on the Default Branch

1. Please open **an issue**, if you have improvement ideas.
1. Create a **merge request** from that issue.
1. Merge contributions after review.

### Changes to workshop related branches

These changes require you to rebase commits and branches locally.
Please double check all your steps.

1. Clone the repository.
1. Checkout all workshop related branches locally.
1. Identify the commit that includes the change set that should be changed.
1. Switch to the branch which includes the aforementioned commit.
1. Apply your contributions in a new or edit an existing commit(s).
1. Ensure the previous commit order is preserved.
1. Rebase all later branches to fix the commit history. 
1. Verify that changes were successful using the checklist below.
1. (Force) Push all effected branches to GitLab.
   - **Warning: This will override the previous commit history**.
   - You may need to ask a maintainer to unprotect the default branch.
1. Recreate Git tag `1.0.0`.
1. If necessary, add additional contributors [here](https://gitlab.com/hifis/hifis-workshops/make-your-code-ready-for-publication/workshop-materials#contributors).


#### Example

We applied a change in the branch `4-add-license-infos` and the commits are already squashed and cleaned.

```
git switch 5<tab> && git rebase 4<tab>
git switch 6<tab> && git rebase 5<tab>
git switch check<tab> && git rebase 6<tab>

# Verify that changes were successful (Use checklist below).

git switch 5<tab> && git push -f
git switch 6<tab> && git push -f

# Verfiy (again) on GitLab that all changes are correct.
# Unprotect default branch on gitlab.
git switch check<tab> && git push -f
```

#### Checklist

- [ ] Commit history is linear.
  Use `git log --graph --all --oneline --decorate`.
- [ ] Review every branch.
  - Verify that no prior change set was lost during the rebase process.
  - Use `git status` to verify that the number of changed local commits match the number on the remote.
