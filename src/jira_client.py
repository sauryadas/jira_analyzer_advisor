from jira import JIRA
from src.config import JIRA_SERVER, JIRA_EMAIL, JIRA_API_TOKEN
import pandas as pd

def fetch_jira_data(project_key, days_back=60, limit=500):
    options = {
        "server": JIRA_SERVER,
        "rest_api_version": "3"
    }

    jira = JIRA(
        options=options,
        basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN)
    )

    print(f"Fetching tickets via /rest/api/3/search/jql...")
    
    jql_query = f'project="{project_key}" AND created >= "-{days_back}d"'
    
    # Use the direct JQL endpoint as requested by the 410 error
    url = f"{JIRA_SERVER}/rest/api/3/search/jql"
    params = {
        "jql": jql_query,
        "maxResults": limit,
        "fields": ["summary", "components", "status", "created", "assignee"] # Specific fields help performance
    }

    # Manually call the correct endpoint
    response = jira._get_json("search/jql", params=params)
    issues_raw = response.get('issues', [])
    
    print(f"Successfully retrieved {len(issues_raw)} issues.")

    # Format the data into the list your DataFrame expects
    issues_data = []
    for issue in issues_raw:
        fields = issue.get('fields', {})
        # Check for the Person Assigned (Assignee)
        assignee_data = fields.get('assignee')
        assignee_name = assignee_data.get('displayName') if assignee_data else "Unassigned"
        
        # Check for the Project Component
        comps = fields.get('components', [])
        comp_name = comps[0].get('name') if comps else "No Component"
        
        issues_data.append({
            'key': issue.get('key'),
            'summary': fields.get('summary'),
            'assignee': assignee_name,  # Track the person
            'component': comp_name,     # Track the category
            'status': fields.get('status', {}).get('name'),
            'created': fields.get('created')
        })

    return pd.DataFrame(issues_data)