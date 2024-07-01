# test-codebase

Recursively traverses a codebase creates unit tests for each code file. After you have solid tests in place, you can use this same script to go through and improve your code, and test the improved code against it.


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

### Create tests

```shell
python -m src.main <path_to_folder> <language: "python" or "javascript">
```

### Improve code

```
python -m src.main <path_to_folder> <language: "python" or "javascript"> True
```