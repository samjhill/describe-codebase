import os
import sys

from src.ai import describe_file_contents
from src.extensions import code_file_extensions

IGNORED_FILES = [".gitignore", "README.md", "requirements.txt"]

def describe_file(file_path):
    description = describe_file_contents(file_path)

    return description

def traverse_directory(directory, language="python"):
    for root, dirs, files in os.walk(directory):
        # Ignore files specified in .gitignore
        if '.gitignore' in files:
            with open(os.path.join(root, '.gitignore'), 'r') as gitignore_file:
                gitignore_content = gitignore_file.read().split('\n')
                files = [f for f in files if f not in gitignore_content]
        
        for file in files:
            if file in IGNORED_FILES:
                continue
            
            file_path = os.path.join(root, file)
            extension = os.path.splitext(file_path)[-1].lower()
            
            if extension not in code_file_extensions:
                continue

            if "tests" in file_path:
                continue

            if ".venv" in file_path:
                continue
            
            if ".json" in file_path:
                continue

            if "mocks" in file_path:
                continue
            
            if "types" in file_path:
                continue

            save_directory = f"{directory}/tests"

            if language == "python":
                description_file = os.path.join(save_directory, f'test_{file.split(".")[0]}.py')
            
            if language == "js" or language == "ts":
                description_file = os.path.join(save_directory, f'{file.split(".")[0]}.test.js')

            # Check if the test file already exists, and if so, skip it
            if os.path.exists(description_file):
                print(f"Skipping {description_file} as it already exists.")
                continue
            
            description = describe_file(file_path)

            if not description or len(description) < 150:
                print("not writing this to file")
                continue
            
            os.path(save_directory).mkdir(parents=True, exist_ok=True)

            with open(description_file, 'w') as desc_file:
                print(description)
                desc_file.write(description)
            
            # python: create init file
            if language == "python":
                with open(f"{save_directory}/__init__.py", 'w') as init_file:
                    init_file.write("")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        repository_path = sys.argv[1]
    else:
        repository_path = "."

    print(f"Running on {repository_path}...")
    
    traverse_directory(repository_path)
