import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Debug: Print which variables are loaded (hide the token for safety)
print(f"DEBUG: Server={os.getenv('JIRA_SERVER')}")
print(f"DEBUG: Email={os.getenv('JIRA_EMAIL')}")
print(f"DEBUG: Token Found={'Yes' if os.getenv('JIRA_API_TOKEN') else 'No'}")

JIRA_SERVER = os.getenv("JIRA_SERVER")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") #

if not all([JIRA_SERVER, JIRA_EMAIL, JIRA_API_TOKEN]):
    raise ValueError("Missing required environment variables. Check your .env file.")