# test-codebase

Recursively traverses a codebase and analyzes each file using GPT-4. It creates a test file for each code file.


## Setup

Clone this repository.

Create a `.env` file at the root of this directory with the following content:

```
OPENAI_API_KEY="...."
```


```shell
python3 -m venv .venv
source .venv/bin/activate
pip install
```

## Usage

```shell
python3 -m main <path_to_folder>
```