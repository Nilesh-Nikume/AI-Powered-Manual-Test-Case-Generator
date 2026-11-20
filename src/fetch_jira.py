import os
import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

print("Hello! Python Script is running")
# Load environment variables
load_dotenv()

# Read Jira credentials
JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

# Jira Issue Key
ISSUE_KEY = "KAN-4"


def fetch_jira_issue():

    # Jira API URL
    url = f"{JIRA_URL}/rest/api/3/issue/{ISSUE_KEY}"

    # Authentication
    auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)

    # Headers
    headers = {
        "Accept": "application/json"
    }

    # API Request
    response = requests.get(
        url,
        headers=headers,
        auth=auth
    )

    # Check response
    if response.status_code == 200:

        data = response.json()

        print("\n========== JIRA ISSUE DETAILS ==========")

        print("Issue Key:", data["key"])

        print("Summary:", data["fields"]["summary"])

        description = data["fields"].get("description")

        print("\nDescription:")

        if description:
            print(description)
        else:
            print("No description found.")

    else:
        print("Error:", response.status_code)
        print(response.text)
print("Hello! Python Script is completed")


if __name__ == "__main__":
    print("Script Started...")
    fetch_jira_issue()
    print("JIRA function executed..")