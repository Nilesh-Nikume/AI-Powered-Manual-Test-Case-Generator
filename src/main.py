import os
import json
import requests

from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth


# Load Jira credentials from .env
load_dotenv()

JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen3:4b"


# Extract text from Jira Description (ADF format)
def extract_text(description):

    if not description:
        return ""

    if isinstance(description, str):
        return description

    text_parts = []

    def extract_recursively(node):

        if isinstance(node, dict):

            if node.get("type") == "text":
                text_parts.append(node.get("text", ""))

            for value in node.values():
                if isinstance(value, (dict, list)):
                    extract_recursively(value)

        elif isinstance(node, list):

            for item in node:
                extract_recursively(item)

    extract_recursively(description)

    return " ".join(text_parts)


# Fetch Jira Issue
def fetch_jira_issue(issue_key):

    url = f"{JIRA_URL}/rest/api/3/issue/{issue_key}"

    auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)

    headers = {
        "Accept": "application/json"
    }

    response = requests.get(
        url,
        headers=headers,
        auth=auth,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    summary = data["fields"]["summary"]

    description = data["fields"].get("description")

    description_text = extract_text(description)

    print("\n========== JIRA DETAILS ==========")
    print("Issue Key:", issue_key)
    print("Summary:", summary)
    print("Description:", description_text)

    return summary, description_text


# Generate Manual Test Cases using Ollama
def generate_test_cases(summary, acceptance_criteria):

    prompt = f"""
    You are an experienced QA Engineer.

    Generate manual test cases based on the following Jira requirement.

    Jira Summary:
    {summary}

    Acceptance Criteria:
    {acceptance_criteria}

    Generate test cases covering:
    1. Positive scenarios
    2. Negative scenarios
    3. Edge cases

    Return ONLY valid JSON.

    Do not include explanations, thinking process or markdown.

    Follow this exact JSON structure:

    {{
        "test_cases": [
            {{
                "test_case_id": "TC_001",
                "scenario": "Test scenario",
                "preconditions": "Preconditions",
                "steps": [
                    "Step 1",
                    "Step 2"
                ],
                "expected_result": "Expected result",
                "test_type": "Positive"
            }}
        ]
    }}
    """

    ollama_url = "http://localhost:11434/api/chat"

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "think": False,
        "format": "json",
        "stream": False,
        "options": {
            "num_predict": 1024,
            "num_ctx": 2048,
            "temperature": 0.2
        }
    }

    response = requests.post(
        ollama_url,
        json=payload,
        timeout=(10, 600)
    )

    response.raise_for_status()

    result = response.json()

    generated_text = result.get("message", {}).get("content", "").strip()

    if not generated_text:
        raise Exception("Ollama returned empty response.")

    try:
        parsed_result = json.loads(generated_text)

    except json.JSONDecodeError:
        raise Exception("Ollama did not return valid JSON.")

    if not isinstance(parsed_result.get("test_cases"), list):
        raise Exception("Invalid test case JSON structure.")

    return parsed_result


# Main Execution
if __name__ == "__main__":

    issue_key = "KAN-4"

    print("Fetching Jira Issue...")

    summary, description = fetch_jira_issue(issue_key)

    if not description:
        print("No Acceptance Criteria found in Jira Description.")

    else:

        print("\nGenerating Manual Test Cases using AI...")

        test_cases = generate_test_cases(
            summary,
            description
        )

        print("\n========== GENERATED MANUAL TEST CASES ==========\n")

        print(test_cases)