from jira import JIRA
from github import Github
import re

# Replace with your actual credentials
JIRA_EMAIL = "krunaltemp1312@gmail.com"
JIRA_API_TOKEN = "ATATT3xFfGF0m2hT76p98PamB2UplDmhIXqR9TZzXpXiA7Xy34mmK7FZu2wNAdIBIQmpl_enwBKKLwYRv6Orf7nlLYfGcEnA0hLmP4gi1SbALogo74_Hg6KveA6RQ-id8zsS1zuiAABRbTxzOvdYq5cztG1QGUPjG9q_RNBK3MaDaHwFct5bnQo=6369861D"
JIRA_SERVER = "https://krunaltemp1312.atlassian.net"
PROJECT_KEY = "KAN"

GITHUB_TOKEN = "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"
REPO_NAME = "Krunalsangani13/Automating-Project-Development-Planning"

# Initialize Jira and GitHub connections
jira_options = {'server': JIRA_SERVER}
jira = JIRA(options=jira_options, basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN))
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

# Fetch Jira tickets
issues = jira.search_issues(f'project={PROJECT_KEY}', maxResults=50)

# Link test cases to Jira tickets
for issue in issues:
    key = issue.key
    summary = issue.fields.summary.strip()
    
    # Clean the summary for safe file names
    clean_summary = re.sub(r"[^a-zA-Z0-9-]+", "-", summary.lower())
    
    # Determine the branch name
    if "epic" in summary.lower():
        branch_name = f"epic/{key}-{clean_summary}"
    elif "task" in summary.lower():
        branch_name = f"task/{key}-{clean_summary}"
    elif "sub-task" in summary.lower():
        branch_name = f"subtask/{key}-{clean_summary}"
    else:
        branch_name = f"feature/{key}-{clean_summary}"
    
    # Construct the GitHub test file path
    test_file_path = f"{branch_name}/tests/test_{clean_summary}.py"
    
    try:
        # Check if the branch exists
        if branch_name not in [branch.name for branch in repo.get_branches()]:
            print(f"⚠️ Branch '{branch_name}' not found. Skipping...")
            continue
        
        # Construct the GitHub URL
        github_url = f"https://github.com/{REPO_NAME}/blob/{branch_name}/{test_file_path}"
        
        # Update the Jira ticket with the GitHub link
        issue.update(fields={"description": f"{issue.fields.description}\n\n📝 **Test File:** [{test_file_path}]({github_url})"})
        print(f"✅ Linked test case for {key}: {github_url}")
    
    except Exception as e:
        print(f"❌ Failed to link test case for {key}: {e}")

print("\n✅ Test case linking complete.")