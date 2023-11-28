from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

def run_prompt(prompt, content, num_tokens=300):
    # Set your OpenAI API key
    api_key = os.environ.get("OPENAI_API_KEY")

    # Initialize the OpenAI API client
    client = OpenAI(
        # defaults to os.environ.get("OPENAI_API_KEY")
        api_key=api_key,
    )

    prompt = f"{prompt} {content}"

    # Call the OpenAI GPT-3 API for analysis
    response = client.chat.completions.create(
        model="gpt-4",
        max_tokens=num_tokens,  # Adjust as needed
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content.strip()


def describe_file_contents(path):
    f = open(path, "r")
    return run_prompt(
        "The following is a piece of code. Please return the output as follows: 1) Summary <general summary of the file's overall function goes here> \n 2) Individual methods <list each method in the same order the file provides, with inputs, outputs, and purpose described> ",
        f.read(),
    )

