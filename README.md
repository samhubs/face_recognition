# Face Recognition with modern tools

This repository covers the following approaches:

1. Data version control (DVC)
2. Poetry
3. Pytorch
4. FastAPI

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