# AIDev Data Processing Scripts

This repository contains Python scripts for processing GitHub pull request data from the AIDev dataset.

## Files

- **humandev.py** - Main script for processing human PR data
- **aidev\_\_testing.py** - Script for testing and comparing different datasets
- **requirements.txt** - Python package dependencies

## Setup
Create an AIDev_shared directory at the root, and drag the files from our shared google drive over.

```bash
pip install -r requirements.txt
```

Required packages:

- pandas
- numpy
- matplotlib
- seaborn
- requests
- python-dateutil
- nest-asyncio
- pyarrow
- polars

### 2. Run the Scripts

#### humandev.py

This script processes human pull request data from HuggingFace and calculates various metrics.

```bash
python humandev.py
```

**Configuration Options:**

Edit the top of `humandev.py` to configure:

```python
# Toggle to TRUE to limit dataset, else process entire dataset
TEST_MODE = True  # Set to False for full dataset

# Toggle to TRUE to reload from disk, else do the preprocessing
RELOAD = True  # Set to False for first run to download data
```

**First Run:**

- Set `RELOAD = False` to download and process data from HuggingFace
- Set `TEST_MODE = True` to test with a smaller dataset first
- Data will be cached in `AIDev_shared/` folder

**Subsequent Runs:**

- Set `RELOAD = True` to use cached data (faster)
- Script will load previously processed pickle files

**Output:**

- Creates `AIDev_shared/control_metrics_TEST.csv` (or `control_metrics.csv` if TEST_MODE=False)
- Contains 19 metrics per pull request

#### aidev\_\_testing.py

This script performs various analyses on the AIDev dataset.

```bash
python aidev__testing.py
```

## Data Folder

All processed data is stored in `AIDev_shared/` directory:

- `metrics_hu.pkl` / `metrics_hu_TEST.pkl` - Cached PR metrics
- `repos_hu.pkl` / `repos_hu_TEST.pkl` - Cached repository data
- `control_metrics.csv` / `control_metrics_TEST.csv` - Final output

## Metrics Calculated

The scripts calculate 19 metrics for each pull request:

### PR Variables

1. **repoLanguage** - Programming language
2. **forkCount** - Number of forks
3. **stargazerCount** - Number of stars
4. **repoAge** - Repository age in days
5. **state** - MERGED or CLOSED
6. **deletions** - Lines of code deleted
7. **additions** - Lines of code added
8. **changedFiles** - Number of files changed
9. **commentsTotalCount** - Total comments
10. **commitsTotalCount** - Number of commits
11. **prExperience** - Author's prior PR count
12. **isMember** - Is author a member
13. **authorComments** - Comments by author
14. **reviewersComments** - Comments by reviewers
15. **reviewersTotalCount** - Number of reviewers
16. **bodyLength** - PR description length
17. **prSize** - Total LOC changed
18. **reviewTime** - Time to review (hours)
19. **purpose** - fix, doc, or feat

## Notes

- The scripts are converted from Google Colab notebooks to run locally
- Data is downloaded from HuggingFace datasets (hao-li/AIDev)
- First run may take longer as it downloads ~100MB+ of data
- Use TEST_MODE for faster testing with smaller dataset
