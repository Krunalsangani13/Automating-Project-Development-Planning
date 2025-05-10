from github import Github

# Replace with your actual GitHub PAT and repository name
GITHUB_TOKEN = "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"
REPO_NAME = "Krunalsangani13/Automating-Project-Development-Planning"

# Jira project key (e.g., KAN)
PROJECT_KEY = "KAN"

# List of sample tickets (replace with actual Jira tickets later)
tickets = [
    {"key": "KAN-2", "summary": "User authentication epic"},
    {"key": "KAN-3", "summary": "User login task"},
    {"key": "KAN-4", "summary": "Validate email input sub-task"},
]

# Initialize GitHub connection
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

# Create branches for each ticket
for ticket in tickets:
    key = ticket["key"]
    summary = ticket["summary"]
    
    # Determine branch name based on ticket type
    if "epic" in summary.lower():
        branch_name = f"epic/{key}-{summary.replace(' ', '-').lower()}"
    elif "task" in summary.lower():
        branch_name = f"task/{key}-{summary.replace(' ', '-').lower()}"
    elif "sub-task" in summary.lower():
        branch_name = f"subtask/{key}-{summary.replace(' ', '-').lower()}"
    else:
        branch_name = f"feature/{key}-{summary.replace(' ', '-').lower()}"

    # Get the main branch to use as the base
    main_branch = repo.get_branch("main")
    
    # Create the branch
    try:
        ref = repo.create_git_ref(
            ref=f"refs/heads/{branch_name}",
            sha=main_branch.commit.sha
        )
        print(f"✅ Created branch: {branch_name}")
    except Exception as e:
        print(f"❌ Failed to create branch {branch_name}: {e}")
