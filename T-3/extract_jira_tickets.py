from jira import JIRA
import re

JIRA_EMAIL = "krunaltemp1312@gmail.com"
JIRA_API_TOKEN = "ATATT3xFfGF0m2hT76p98PamB2UplDmhIXqR9TZzXpXiA7Xy34mmK7FZu2wNAdIBIQmpl_enwBKKLwYRv6Orf7nlLYfGcEnA0hLmP4gi1SbALogo74_Hg6KveA6RQ-id8zsS1zuiAABRbTxzOvdYq5cztG1QGUPjG9q_RNBK3MaDaHwFct5bnQo=6369861D"
JIRA_SERVER = "https://krunaltemp1312.atlassian.net"
PROJECT_KEY = "KAN"

# Initialize Jira connection
jira_options = {'server': JIRA_SERVER}
jira = JIRA(options=jira_options, basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN))

# Fetch Jira tickets
issues = jira.search_issues(f'project={PROJECT_KEY}', maxResults=50)

# Extract ticket data
tickets = []
for issue in issues:
    key = issue.key
    summary = issue.fields.summary.strip()
    description = issue.fields.description.strip() if issue.fields.description else "No description"
    
    # Clean the summary for safe file names
    clean_summary = re.sub(r"[^a-zA-Z0-9-]+", "-", summary.lower())
    
    # Generate a simple test case
    test_case = f"""
def test_{clean_summary}():
    # Given: {summary}
    # When: {description.split('.')[0]}
    # Then: Add your test logic here
    assert True  # Replace with actual test logic
"""
    tickets.append({
        "key": key,
        "summary": summary,
        "description": description,
        "test_case": test_case.strip()
    })

# Save tickets to a file (for easy reference)
with open("jira_tickets.txt", "w") as f:
    for ticket in tickets:
        f.write(f"{ticket['key']} - {ticket['summary']}\n")
        f.write(f"{ticket['test_case']}\n\n")

print("✅ Jira tickets extracted and saved to jira_tickets.txt")