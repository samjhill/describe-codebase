# test-codebase

Recursively traverses a codebase creates unit tests for each code file.


## Setup

Clone this repository.

Create a `.env` file at the root of this directory with the following content:

```
OPENAI_API_KEY="...."
```


```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```shell
python -m src.main <path_to_folder>
```