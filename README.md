# Face Recognition with modern tools

This repository covers the following approaches:

1. Data version control (DVC)
2. Poetry
3. Pytorch
4. VSCode with LambdaLabs extension
5. FastAPI
6. Github Actions
7. Dotenv

## Poetry Setup
1. Install poetry
```sh
curl -sSL https://install.python-poetry.org | python3 -
```
2. Navigate to the local Git repository and initialize a `poetry` project:
```sh
poetry init
```
The prompts will guide you to provide relevant information as below

![alt text](/utils/poetry_guide.png)

3. Add dependencies to pyproject.toml under `[tool.poetry.dependencies]` section. 

4. Install dependencies
```sh
poetry install
```
If you want to use poetry for managing dependies alone, you can set `package-mode = false` in `pyproject.toml` file under `[tool.poetry]`.

## DVC Setup
1. Install dvc in the virtual environment
```sh
pip install dvc dvc[gdrive]
```
2. Initialize dvc in the root directory of the project
```sh
dvc init
```
3. Associate the remote location with dvc (we are using Google Drive in this case)
```sh
dvc remote add --default <remote name> <remote url>
```
provide a custom name as `<remote name>`. To find out `remote url`: 
  - navigate to the Google Drive folder and fetch the `id` from the address bar. For example, you will see a url like this: `https://drive.google.com/drive/u/1/folders/1jos7TNeasdfd45545353P`, where the `id` corresponds to the end part, i.e. `1jos7TNeasdfd45545353P`. 

  - assemble the url as `gdrive://1jos7TNeasdfd45545353P`.
4. Authenticate using a Google Service Account
    - set up a service account following this [official link](https://dvc.org/doc/user-guide/data-management/remote-storage/google-drive#using-service-accounts) using Google Cloud Platform (GCP)
    - enable `Google Drive API` using `API and Services`
    - creat a new key and download .JSON with credentials and save them to a local directory
    - set up an environment variable with key `GDRIVE_CREDENTIALS_DATA` and value being the content of the JSON. 
    - share the `Google Drive` folder with the service account email, that should look something like this: gdrive-dvc-auth@my-project.iam.gserviceaccount.com
    - set remote to use service accounts:
    ```sh
    dvc remote modify <remote name> gdrive_use_service_account true
    ```

5. Check if authentication passes by running a status command: 
    ```sh
    dvc status -c
    
    # If you have a local folder that you would like to push, use `dvc add <folder path>` and `dvc push`, else, perform `dvc pull` to fetch the data from remote - a process similar to `git`
    ```
  if you face an issue, please use `Troubleshooting tips` below.

## 2. Running DVC with CI (Github actions)
There are two ways in which CI runs are set up in this repository: 1) locally using `act`, and 2) on `GitHub`. Both the ways employ Github actions ([see here](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python)). Let's start with setting up CI runs using [act](https://github.com/nektos/act).

a) Using `act`

When a CI run is configured with `.github/workflows/ci.yml`, `act` reads the yml file and determines the set of jobs or actions that are required to be run locally. This means `act` has to emulate all the functionalities that are set up on `Github` including `dvc` on the local machine. Here are the steps:

```sh
# 1. check workflow
act -l

# 2. update the dvc configuration in the ci.yml to take care of dvc configs
  name: Pull DVC managed files
    run: |
        env
        echo "Configuring DVC remote"
        dvc remote modify gdrive gdrive_use_service_account true
        echo "${GDRIVE_CREDENTIALS_DATA}" > gdrive_credentials.json
        dvc remote modify gdrive gdrive_service_account_json_file_path \
                       gdrive_credentials.json
        echo "Pulling DVC managed files"
        dvc pull -v

# 3. run the job as per .github/workflow/ci.yml. The example here is for MacOS M2 chip
act --container-architecture linux/amd64 -s \
GDRIVE_CREDENTIALS_DATA="$GDRIVE_CREDENTIALS_DATA"
```  

## Troubleshooting
- Local runs:
    - If authentication fails while using any of the `dvc` commands:
        - ensure `GDRIVE_CREDENTIALS_DATA` is set up as a local environment variable.  
          ```sh
          echo $GDRIVE_CREDENTIALS_DATA
          ```
        - check if `Google Drive API` is enabled in the service account on GCP 
        - Clear cache and retry, typically, cache is found at: `$CACHE_HOME/pydrive2fs/{gdrive_client_id}/default.json`
- CI with [act](https://github.com/nektos/act):
    
    - secrets are to be supplied with `-s` option
    - if you have functions that require `GITHUB_TOKEN`, you can skip the function as:
    ```sh
      - name: Report test results to Test Reporter
        uses: dorny/test-reporter@v1
        if: always() && env.ACT_RUN != 'true'
        with:
          name: generate test reports
          path: test-results/*.xml
          reporter: java-junit
          fail-on-error: false
          fail-on-empty: false
          token: ${{ secrets.GITHUB_TOKEN }}


## Github Actions

1. Create a `.github/workflows` directory in the root of the repository.

2. Create a `ci.yml` file in the `.github/workflows` directory and add the following code:
```yml
name: Face Recognition CI

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
    build:
        runs-on: ubuntu-latest
    
        steps:
        - uses: actions/checkout@v2
        - name: Set up Python 3.8
        uses: actions/setup-python@v2
        with:
            python-version: 3.8
        - name: Install dependencies
        run: |
            python -m pip install --upgrade pip
            pip install -r requirements.txt
        - name: Run tests
        run: |
            pytest
    ```

