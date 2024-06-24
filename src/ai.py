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

def extract_imports(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    import_lines = []
    import_pattern = re.compile(r'^\s*(import|from)\s+')

    for line in lines:
        if import_pattern.match(line):
            import_lines.append(line.strip())
        else:
            # Stop collecting if a non-import statement is encountered
            if line.strip():  # Ignore blank lines
                break

    return import_lines

def split_methods(file_path):
    with open(file_path, 'r') as file:
        code = file.read()

    # Use regex to find all method definitions and their bodies
    method_pattern = re.compile(r'(^def\s+.*?:\n(?:\s{4,}.*\n*)*)', re.MULTILINE)
    methods = method_pattern.findall(code)
    
    return methods

def describe_file_contents(file_path, language="python"):
    test_type = "pytest" if language == "python" else "Jest"
    print(f"running on {file_path}")

    imports = extract_imports(file_path)
    methods = split_methods(file_path)
    test_results = []
    
    for method in methods:
        result = run_prompt(f"The following is a piece of code. Please act as an expert programmer and write {test_type} unit tests for it. Consider all edge-cases that you can. Only return the raw code of the tests; do not add any commentary before or after. Do not wrap the response in backticks (`). If there are no functions to test, simply return an empty string.",
            method,
        )
        print(result)
        test_results.append(result)

    joined_results = ('\n \n').join(test_results)
    joined_imports = ('\n').join(imports)

    return (f"{joined_imports} \n \n {joined_results}")

