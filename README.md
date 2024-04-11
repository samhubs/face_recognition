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

