import os
import sys

from ai import describe_file_contents

IGNORED_FILES = [".gitignore", "README.md", "requirements.txt"]

def describe_file(file_path):
    description = describe_file_contents(file_path)

    return description

def traverse_directory(directory):
    for root, dirs, files in os.walk(directory):
        # Ignore files specified in .gitignore
        if '.gitignore' in files:
            with open(os.path.join(root, '.gitignore'), 'r') as gitignore_file:
                gitignore_content = gitignore_file.read().split('\n')
                files = [f for f in files if f not in gitignore_content]

        # Create a folder for descriptions in each level
        description_folder = os.path.join(root, 'descriptions')
        os.makedirs(description_folder, exist_ok=True)

        for file in files:
            if file in IGNORED_FILES:
                continue

            file_path = os.path.join(root, file)
            description = describe_file(file_path)

            # Save description to a file
            description_file = os.path.join(description_folder, f'{file}-description.txt')
            with open(description_file, 'w') as desc_file:
                desc_file.write(description)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        repository_path = sys.argv[1]
    else:
        repository_path = "."

    print(f"Running on {repository_path}...")
    
    traverse_directory(repository_path)
