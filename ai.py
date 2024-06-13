from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

def run_prompt(prompt, content, num_tokens=1250):
    # Set your OpenAI API key
    api_key = os.environ.get("OPENAI_API_KEY")

    # Initialize the OpenAI API client
    client = OpenAI(
        # defaults to os.environ.get("OPENAI_API_KEY")
        api_key=api_key,
    )

    prompt = f"{prompt} {content}"

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        max_tokens=num_tokens,  # Adjust as needed
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content.strip()


def describe_file_contents(path):
    f = open(path, "rb")
    contents = f.read()
    print(f"running on {path}")
    return run_prompt(
        "The following is a piece of code. Please act as an expert programmer and write Jest unit tests for each function in the file. Only return the raw code of the tests; do not add any commentary before or after. Do not wrap the response in backticks (`). If there are no functions to test, simply return an empty string.",
        contents,
    )

