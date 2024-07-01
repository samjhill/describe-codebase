import os
import re
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

def run_prompt(prompt, content, num_tokens=750):
    # Set your OpenAI API key
    api_key = os.environ.get("OPENAI_API_KEY")

    client = OpenAI(
        api_key=api_key,
    )

    prompt = f"{prompt} {content}"

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        max_tokens=num_tokens,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content.strip()

def extract_before_first_method(file_path):
    """
    Extracts everything before the first method definition in a Python file.

    :param file_path: Path to the Python file.
    :return: A string containing the content before the first method definition.
    """
    before_first_method = []
    def_pattern = re.compile(r'^\s*def\s+')

    with open(file_path, 'r') as file:
        lines = file.readlines()

        for line in lines:
            if def_pattern.match(line):
                break
            before_first_method.append(line)

    return ''.join(before_first_method)

def split_methods(file_path):
    with open(file_path, 'r') as file:
        code = file.read()

    # Use regex to find all method definitions and their bodies
    method_pattern = re.compile(r'(^def\s+.*?:\n(?:\s{4,}.*\n*)*)', re.MULTILINE)
    methods = method_pattern.findall(code)
    
    return methods

def describe_file_contents(file_path, parent_directory, improve_code=False, language="python"):
    test_type = "pytest" if language == "python" else "Jest"
    print(f"running on {file_path}")

    methods = split_methods(file_path)
    imports = extract_before_first_method(file_path)
    relative_path = os.path.relpath(file_path, parent_directory)

    test_results = []
    
    test_prompt = f"The following is a piece of code. Please act as an expert programmer and write {test_type} unit tests for it. Whenever you need to patch a custom module, use the path to the module: {relative_path}. Ensure there are no misspellings and that all called methods and properties exist and are consistently named throughout the code. Only return the raw code of the tests; do not add any commentary before or after. Do not wrap the response in backticks (`). If there are no functions to test, simply return an empty string. Ensure that any renamed methods or properties are updated consistently throughout the code."
    
    improve_code_prompt = f"The following is a piece of code. Please act as an expert programmer and improve the code, making it more readable. Ensure there are no misspellings and that all called methods and properties exist and are consistently named throughout the code. Only return the raw code; do not add any commentary or wrap the response in backticks (`). If there are no functions to test, simply return an empty string. Ensure that any renamed methods or properties are updated consistently throughout the code."

    for method in methods:
        result = run_prompt(improve_code_prompt if improve_code else test_prompt,
            method,
        )
        print(result)
        test_results.append(result)

    joined_results = ('\n \n').join(test_results)

    if len(joined_results) < 1:
        return False
    
    return (f"{imports} \n \n{joined_results}")

