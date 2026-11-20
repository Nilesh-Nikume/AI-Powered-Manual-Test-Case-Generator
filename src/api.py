from fastapi import FastAPI, HTTPException
import requests

from src.main import fetch_jira_issue, generate_test_cases

app = FastAPI(
    title="AI Manual Test Case Generator",
    description="Generate Manual Test Cases from Jira using Ollama",
    version="1.0"
)


@app.get("/")
def home():
    return {
        "message": "AI Manual Test Case Generator API is running"
    }


@app.get("/generate/{issue_key}")
def generate(issue_key: str):

    try:
        # Step 1: Fetch Jira Issue
        summary, description = fetch_jira_issue(issue_key)

        if not description:
            raise HTTPException(
                status_code=404,
                detail="Jira Description not found"
            )

        # Step 2: Generate Test Cases using AI
        test_cases = generate_test_cases(
            summary,
            description
        )

        # Step 3: Return Response
        return {
            "issue_key": issue_key,
            "summary": summary,
            "generated_test_cases": test_cases
        }

    except requests.exceptions.HTTPError as error:
        raise HTTPException(
            status_code=502,
            detail=f"Jira API error: {str(error)}"
        )

    except requests.exceptions.RequestException as error:
        raise HTTPException(
            status_code=502,
            detail=f"Connection error: {str(error)}"
        )

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )