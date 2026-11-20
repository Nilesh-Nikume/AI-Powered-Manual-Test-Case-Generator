import requests

# Ollama API URL
OLLAMA_URL = "http://localhost:11434/api/generate"

# Model name
MODEL_NAME = "qwen3:4b"


def generate_test_cases(acceptance_criteria):

    prompt = f"""
    You are an experienced QA Automation Engineer.

    Convert the following Acceptance Criteria
    into detailed Manual Test Cases.

    Acceptance Criteria:
    {acceptance_criteria}

    Generate test cases with:

    1. Test Case ID
    2. Test Scenario
    3. Preconditions
    4. Test Steps
    5. Expected Result
    6. Test Type (Positive/Negative/Edge Case)

    Generate clear and detailed test cases.
    """

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options":{"num_predict": 256,
                   "num_ctx": 2048,
                   "temperature": 0.2}
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=(10,600)
    )

    response.raise_for_status()

    ollama_result = response.json()

    print("\n========== OLLAMA RAW RESPONSE ==========")
    print(ollama_result)

    generated_text = ollama_result.get("response", "")

    print("\n========== GENERATED TEXT ==========")
    print(generated_text)

    return generated_text


if __name__ == "__main__":

    acceptance_criteria = """
    User should be able to login using valid credentials.
    User should see an error message for invalid credentials.
    """

    print("Generating Manual Test Cases...")

    test_cases = generate_test_cases(acceptance_criteria)

    print("\n========== GENERATED TEST CASES ==========\n")

    print(test_cases)