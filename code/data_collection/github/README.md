# Code Collection Pipeline

This section is the Pipeline for Python code collection. The main workflow includes: using [Github GraphQL API](https://docs.github.com/en/graphql) to obtain repository information, downloading repositories and extracting data, and finally cleaning and packaging the data. The implementation of the data processing part refers to [Code Parrot](https://github.com/huggingface/transformers/blob/main/examples/research_projects/codeparrot).



## Installation

Basic environment

```
numpy
datasets
transformers
datasketch
dpu-utils
tqdm 
```



## Usage

- To use the Github API, you need to have a Github account and apply for a Personal Access Token. [How to apply?](https://docs.github.com/en/enterprise-server@3.9/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
- Enter the Token you applied for on line 8 of `gh_crawler.py` (replace \*TOKEN\*)
- In `collect_data.sh`, you can customize several parameters, including:
  - `LANG`: Define the programming language type to collect (note: the data processing part is designed for the Python language, other languages may require changes to the data processing workflow)
  - `NUM_REPOS`: Define the number of repositories to collect
  - `MIN_STARS`: Define the minimum number of stars of the repositories to ensure the quality of the repositories
  - `CREATED_AT`: Define the creation time of the repositories to collect
- Finally, run the entire pipeline with `bash collect_data.sh` and the collected data will be saved under folder `ProcessedData/data`.