# Contribution Guideline


## Picking Issues to Work on
Once you have gone through the steps in the [README.md](https://github.com/bricct/bracs-api/blob/main/README.md) and have everything set up, it's time for you to get cracking! To do that: 

1. Go to the Issue tracker to find something to work on 
2. Once you have found an issue, assign yourself to that issue so that the other contributors know that you are working on that issue 

## Creating another branch
1. Near the bottom right of an issue page, under *Development*, you will see a hyperlink saying "Create a branch for this issue or link a pull request". Click on it and follow the on screen instructions to create a new branch for the issue. With this, the issue will automatically close after you finish your work. 
2. If you are planning on making a contribution that doesn't correspond to any issues in the tracker and you don't feel like making a new issue, you can instead create another branch off of main and go into it with a command like `git checkout main && git checkout -b mywork`.
3. Pull in any updates to the code using `git pull origin main`

## Before Committing
Before committing your work, navigate to the root directory of the project and run **`make fmt`**. This will require you to install certain Python packages that lint and reformat your code according to this repository's style guidelines.

These packages include isort, autoflake, autopep8, and black.

## Pull Requests 
1. After committing your work to your branch, navigate to the bracs Github page and open a new pull request for your branch
2. If it passes all checks, request a review from any maintainer.
3. Once you have your approval, the collaborator that reviewed your PR will merge it!
