# AI-Powered Manual Test Case Generator

A GenAI-based QA utility that fetches a Jira issue, sends its
requirement/description to a locally hosted Large Language Model (LLM)
through Ollama, and returns structured manual test cases through a
FastAPI REST API.

This project demonstrates how Jira, Python, a local LLM, FastAPI, and
Postman can work together in a practical QA workflow.

## Project Overview

Manual test case preparation from Jira requirements can be repetitive
and time-consuming. This project helps QA engineers create an initial
set of structured manual test cases from a Jira issue.

The application:

1.  Accepts a Jira issue key, such as `KAN-4`.
2.  Fetches the issue summary and description using the Jira REST API.
3.  Sends the requirement text to a locally running Qwen model through
    Ollama.
4.  Requests test cases in a structured JSON format.
5.  Returns the generated test cases through a FastAPI endpoint.
6.  Allows the endpoint to be tested using Swagger UI or Postman.

> **Current implementation note:** The current workflow sends the Jira
> issue's complete Description field to the LLM. The Acceptance Criteria
> (AC) are maintained inside that Description. Extracting only the AC
> section can be added as a future enhancement.

## Technology Stack

  Technology        Purpose
  ----------------- -------------------------------------------------
  Python            Main programming language
  Jira REST API     Fetch Jira issue details
  `requests`        Send HTTP requests to Jira and Ollama
  `python-dotenv`   Load Jira credentials from a local `.env` file
  Ollama            Run the language model locally
  Qwen model        Generate manual test cases from the requirement
  FastAPI           Expose the generator as a REST API
  Uvicorn           Run the FastAPI application
  Postman           Send API requests and validate responses
  Swagger UI        Explore and execute the API interactively

## High-Level Workflow

``` text
                 QA Engineer
                      |
                      | Jira Issue Key (e.g. KAN-4)
                      v
                 Postman / Swagger
                      |
                      | GET /generate/{issue_key}
                      v
                 FastAPI (api.py)
                      |
                      v
              Python Jira Integration
                  (main.py)
                      |
                      | Jira REST API request
                      v
                  Jira Cloud
                      |
                      | Issue Summary + Description
                      v
              Python Test Case Generator
                  (main.py)
                      |
                      | Prompt + requirement
                      v
                Ollama Local API
                (Qwen LLM Model)
                      |
                      | Structured JSON output
                      v
                 FastAPI Response
                      |
                      v
                 Postman / Swagger
                Generated Test Cases
```

## Features

-   Fetches Jira issue summary and description dynamically using an
    issue key.
-   Uses Jira API token authentication through environment variables.
-   Uses a locally hosted Qwen model through Ollama.
-   Generates manual test cases from Jira requirements.
-   Prompts the model to cover positive, negative, and edge-case
    scenarios.
-   Requests structured JSON output containing:
    -   Test Case ID
    -   Scenario
    -   Preconditions
    -   Test Steps
    -   Expected Result
    -   Test Type (Positive / Negative / Edge Case)
-   Exposes the workflow through a FastAPI REST endpoint.
-   Supports testing through Swagger UI and Postman.

## Prerequisites

Install or configure the following before running the project:

-   Python 3.10 or later (recommended)
-   Git
-   Ollama for your operating system
-   A Jira Cloud account with access to the target project and issue
-   A Jira API token
-   Postman (optional; Swagger UI can also be used)

The Qwen model tag used in the Python configuration must match the exact
model name shown by `ollama list`. The examples below use `qwen3:4b`;
replace it if your installed model has a different tag, such as a Qwen
3.5 tag.

## Project Structure

The structure below represents the files used in the current workflow.
Adjust names if your local project differs.

``` text
AI-Manual-Test-Case-Generator/
│
├── .env                         # Local Jira credentials (never commit)
├── .gitignore
├── requirements.txt
├── README.md
│
└── src/
    ├── __init__.py              # Optional; supports package imports
    ├── fetch_jira.py            # Standalone Jira fetch test
    ├── generate_test_cases.py   # Standalone Ollama generation test
    ├── main.py                  # Jira + Ollama integration functions
    └── api.py                   # FastAPI application and endpoint
```

## Setup and Installation

### 1. Clone the repository

``` bash
git clone https://github.com/<your-username>/<your-repository>.git
cd <your-repository>
```

### 2. Create and activate a virtual environment (recommended)

**Windows PowerShell:**

``` powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

``` bat
python -m venv venv
venv\Scripts\activate
```

### 3. Install Python dependencies

Create a `requirements.txt` file in the project root:

``` text
requests
python-dotenv
fastapi
uvicorn
```

Install the dependencies:

``` bash
pip install -r requirements.txt
```

Alternatively, install them directly:

``` bash
pip install requests python-dotenv fastapi uvicorn
```

### 4. Install and verify Ollama

Install Ollama from the official website:

https://ollama.com/

Check that it is installed:

``` bash
ollama --version
```

Download a Qwen model. Example:

``` bash
ollama pull qwen3:4b
```

Start the model and test it:

``` bash
ollama run qwen3:4b
```

Try a prompt such as:

``` text
Generate two manual test cases for login functionality.
Include positive and negative scenarios, steps, and expected results.
```

Check downloaded models:

``` bash
ollama list
```

Check currently loaded/running models:

``` bash
ollama ps
```

> Use the exact model tag shown by `ollama list` in `src/main.py`. For
> example, if the installed tag is `qwen3.5:4b`, configure
> `MODEL_NAME = "qwen3.5:4b"` rather than `qwen3:4b`.

### 5. Configure Jira credentials

Create a `.env` file in the project root (same level as the `src`
folder):

``` env
JIRA_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your-jira-account-email
JIRA_API_TOKEN=your-jira-api-token
```

Replace the example values with your own Jira details.

**Security:** - Never commit `.env` to GitHub. - Never paste your Jira
API token into source code. - Never share screenshots or logs that
expose the token. - If a token is accidentally published, revoke it in
Jira and create a new one.

Example `.gitignore`:

``` gitignore
.env
venv/
.venv/
__pycache__/
*.py[cod]
.idea/
```

### 6. Configure the Ollama model

In `src/main.py`, set the model name to the exact tag shown by
`ollama list`:

``` python
MODEL_NAME = "qwen3:4b"
```

Change the example value if your installed model tag is different.

## Run the Application

### 1. Start Ollama

Make sure Ollama is running. If the Ollama application/service is not
already running, start it using the normal method for your operating
system. In a terminal, you can use:

``` bash
ollama serve
```

If Ollama is already running as a background service, you do not need to
start a second server.

### 2. Start FastAPI

From the **project root directory**, run:

``` bash
python -m uvicorn src.api:app --reload
```

Expected local server address:

``` text
http://127.0.0.1:8000
```

Stop the server with `Ctrl + C`.

### 3. Open Swagger UI

Open this address in a browser:

``` text
http://127.0.0.1:8000/docs
```

The current API exposes:

  -------------------------------------------------------------------------
  Method                  Endpoint                  Purpose
  ----------------------- ------------------------- -----------------------
  GET                     `/`                       Check whether the API
                                                    is running

  GET                     `/generate/{issue_key}`   Fetch a Jira issue and
                                                    generate test cases
  -------------------------------------------------------------------------

### 4. Test using Postman

Set the method to `GET` and use:

``` text
http://127.0.0.1:8000/generate/KAN-4
```

Replace `KAN-4` with an issue key that your Jira account is authorized
to access.

Click **Send**. The API should return the issue key, summary, and
generated test cases in the JSON response.

Example response shape (illustrative only):

``` json
{
    "issue_key": "KAN-4",
    "summary": "Create Test Cases For Login",
    "generated_test_cases": {
        "test_cases": [
            {
                "test_case_id": "TC_001",
                "scenario": "User logs in with correct username and password",
                "preconditions": "User has valid credentials",
                "steps": [
                    "Enter valid username in the username field",
                    "Enter valid password in the password field",
                    "Click on the Login button"
                ],
                "expected_result": "User is successfully logged in and redirected to the dashboard",
                "test_type": "Positive"
            },
            {
                "test_case_id": "TC_0:02",
                "scenario": "User logs in with incorrect password",
                "preconditions": "User has valid username but incorrect password",
                "steps": [
                    "Enter valid username in the username field",
                    "Enter incorrect password in the password field",
                    "Click on the Login button"
                ],
                "expected_result": "User is shown an error message indicating incorrect password",
                "test_type": "Negative"
            },
            {
                "test_case_id": "TC_003",
                "scenario": "User logs in with incorrect username",
                "preconditions": "User has incorrect username but valid password",
                "steps": [
                    "Enter incorrect username in the username field",
                    "Enter valid password in the password field",
                    "Click on the Login button"
                ],
                "expected_result": "User is shown an error message indicating incorrect username",
                "test_type": "Negative"
            },
            {
                "test_case_id": "TC_004",
                "scenario": "User attempts to login with 3 incorrect passwords",
                "preconditions": "User has valid username but 3 incorrect passwords entered",
                "steps": [
                    "Enter valid username in the username field",
                    "Enter incorrect password 1",
                    "Click on Login button",
                    "Enter incorrect password 2",
                    "Click on Login button",
                    "Enter incorrect password 3",
                    "Click on Login button"
                ],
                "expected_result": "User account is locked after the 3rd failed attempt and cannot log in",
                "test_type": "Edge"
            },
            {
                "test_case_id": "TC_005",
                "scenario": "User attempts to login with 2 incorrect passwords",
                "preconditions": "User has valid username but 2 incorrect passwords entered",
                "steps": [
                    "Enter valid username in the username field",
                    "Enter incorrect password 1",
                    "Click on Login button",
                    "Enter incorrect password 2",
                    "Click on Login button"
                ],
                "expected_result": "User is allowed to attempt login again after 2 failed attempts",
                "test_type": "Edge"
            }
        ]
    }
}
```

The actual response depends on the Jira issue content and the model
output.

## Useful Commands Reference

### Ollama

  -----------------------------------------------------------------------
  Command                             Purpose
  ----------------------------------- -----------------------------------
  `ollama --version`                  Display the installed Ollama
                                      version

  `ollama list`                       List locally available models and
                                      their exact tags

  `ollama pull qwen3:4b`              Download the example Qwen model

  `ollama run qwen3:4b`               Run the model interactively in the
                                      terminal

  `ollama ps`                         Show models currently loaded by
                                      Ollama

  `ollama stop qwen3:4b`              Stop the specified running model

  `ollama rm qwen3:4b`                Remove a locally downloaded model

  `ollama serve`                      Start the Ollama server when it is
                                      not already running
  -----------------------------------------------------------------------

### Python and dependencies

  Command                             Purpose
  ----------------------------------- ----------------------------------
  `python --version`                  Display Python version
  `pip --version`                     Display pip version
  `pip list`                          List installed Python packages
  `pip install requests`              Install the HTTP client library
  `pip install python-dotenv`         Install `.env` support
  `pip install fastapi`               Install FastAPI
  `pip install uvicorn`               Install the ASGI server
  `pip install -r requirements.txt`   Install all project dependencies

### Project execution and Windows terminal

  ------------------------------------------------------------------------------
  Command                                    Purpose
  ------------------------------------------ -----------------------------------
  `python src/fetch_jira.py`                 Run the standalone Jira fetch
                                             script (if configured)

  `python src/generate_test_cases.py`        Run the standalone Ollama test-case
                                             script (if configured)

  `python -m uvicorn src.api:app --reload`   Start the FastAPI development
                                             server from the project root

  `Ctrl + C`                                 Stop the running server

  `cls`                                      Clear the Windows Command Prompt

  `dir`                                      List files and folders in the
                                             current directory

  `cd src`                                   Change to the `src` directory

  `cd ..`                                    Move up one directory

  `where python`                             Show the Python executable path

  `netstat -ano \| findstr :8000`            Find the process listening on port
                                             8000
  ------------------------------------------------------------------------------

### Local URLs

  ----------------------------------------------------------------------------
  URL                                      Purpose
  ---------------------------------------- -----------------------------------
  `http://127.0.0.1:8000/`                 API health/root endpoint

  `http://127.0.0.1:8000/docs`             Swagger UI

  `http://127.0.0.1:8000/openapi.json`     OpenAPI specification

  `http://127.0.0.1:8000/generate/KAN-4`   Generate test cases for Jira issue
                                           `KAN-4`
  ----------------------------------------------------------------------------

## Troubleshooting

### 1. Jira authentication or issue-fetch error

Check: - `JIRA_URL`, `JIRA_EMAIL`, and `JIRA_API_TOKEN` in the root
`.env` file. - The Jira issue key is correct. - The Jira account has
permission to view the issue. - The `.env` file is in the project root
and is loaded by the application.

Do not expose the API token when sharing logs.

### 2. Ollama connection error

Check that Ollama is running and that the local API is available at:

``` text
http://localhost:11434
```

Check installed models:

``` bash
ollama list
```

Confirm that `MODEL_NAME` in `src/main.py` exactly matches the installed
model tag.

### 3. Empty generated output

Check the FastAPI terminal for the underlying error. Confirm that the
Ollama response contains generated content and that the application
reads the correct response field. Do not treat HTTP `200 OK` alone as
proof that test cases were generated; verify that the
`generated_test_cases` field contains actual test cases.

### 4. Slow response

Local LLM speed depends on the model size, available RAM/VRAM, CPU,
context length, and prompt size. A smaller model may respond faster, but
output quality should also be reviewed.

### 5. Port 8000 is already in use

Stop the other process using port 8000, or start this application on
another port:

``` bash
python -m uvicorn src.api:app --reload --port 8001
```

Then use `http://127.0.0.1:8001` as the base URL.

## Important Notes and Limitations

-   AI-generated test cases are suggestions and must be reviewed by a QA
    engineer before use.
-   The model may infer scenarios that are not explicitly specified in
    the Jira requirement. Validate expected behavior with the product
    owner or requirement owner.
-   The current implementation sends the full Jira Description to the
    model; it does not yet isolate only the Acceptance Criteria section.
-   The current endpoint uses `GET` for demonstration and learning. For
    a production design, consider a `POST` endpoint for a generation
    operation.
-   Keep Jira credentials in environment variables and never publish
    secrets.
-   The local model runs on the developer's machine; API performance
    varies by hardware and model configuration.

## Future Enhancements

Possible future improvements include:

-   Extract only the Acceptance Criteria section from Jira Description.
-   Export generated test cases to Excel.
-   Add stronger validation for positive, negative, and edge-case
    coverage.
-   Add structured logging and improved error handling.
-   Add automated tests for the API and response schema.
-   Add a `POST` endpoint for test-case generation.

## Author

**Nilesh Nikume**

QA Automation Engineer \| Python \| Selenium \| Jira \| GenAI Testing

Add your GitHub repository URL and LinkedIn profile URL here after
publishing the project.

## Disclaimer

This is a learning and portfolio project demonstrating a GenAI-assisted
QA workflow. Generated test cases are not guaranteed to be complete or
correct and should always be reviewed by a qualified tester.
