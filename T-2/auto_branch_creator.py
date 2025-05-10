from jira import JIRA
from github import Github
import re
import sys
from docx import Document

# Replace with your actual credentials
JIRA_EMAIL = "krunaltemp1312@gmail.com"
JIRA_API_TOKEN = "ATATT3xFfGF0m2hT76p98PamB2UplDmhIXqR9TZzXpXiA7Xy34mmK7FZu2wNAdIBIQmpl_enwBKKLwYRv6Orf7nlLYfGcEnA0hLmP4gi1SbALogo74_Hg6KveA6RQ-id8zsS1zuiAABRbTxzOvdYq5cztG1QGUPjG9q_RNBK3MaDaHwFct5bnQo=6369861D"
JIRA_SERVER = "https://krunaltemp1312.atlassian.net"
PROJECT_KEY = "KAN"

GITHUB_TOKEN = "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"
REPO_NAME = "Krunalsangani13/Automating-Project-Development-Planning"

# Extract requirements from DOCX
def extract_from_docx(path):
    doc = Document(path)
    return [p.text.strip() for p in doc.paragraphs if p.text.strip()]


def main():
    # Check if requirements are available
    doc_path = r"C:\Users\dell\3D Objects\task-2\TASK_2\requirements.docx"
    reqs = extract_from_docx(doc_path)
    if not reqs:
        print(f"⚠️ No requirements found in `{doc_path}`. Exiting without creating branches or files.")
        sys.exit(0)

    # Initialize Jira and GitHub connections
    jira_options = {'server': JIRA_SERVER}
    jira = JIRA(options=jira_options, basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN))
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)

    # Fetch Jira tickets
    issues = jira.search_issues(f'project={PROJECT_KEY}', maxResults=50)

    # Create branches for each ticket
    for issue in issues:
        key = issue.key
        summary = issue.fields.summary
        
        # Determine branch type based on ticket type
        clean_summary = re.sub(r"[^a-zA-Z0-9-]+", "-", summary.strip().lower())
        if "epic" in summary.lower():
            branch_name = f"epic/{key}-{clean_summary}"
        elif "task" in summary.lower():
            branch_name = f"epic/{key}-{clean_summary}"
        elif "sub-task" in summary.lower():
            branch_name = f"epic/{key}-{clean_summary}"
        else:
            branch_name = f"epic/{key}-{clean_summary}"
        
        # Check if the branch already exists
        branches = [branch.name for branch in repo.get_branches()]
        if branch_name in branches:
            print(f"⚠️ Branch '{branch_name}' already exists. Skipping...")
            continue
        
        # Create the branch
        try:
            main_branch = repo.get_branch("main")
            ref = repo.create_git_ref(
                ref=f"refs/heads/{branch_name}",
                sha=main_branch.commit.sha
            )
            print(f"✅ Created branch: {branch_name}")

            # Create directory structure
            files = {
                f"{branch_name}/README.md": f"# {summary}\n\nDescription for {key} - {summary}",
                f"{branch_name}/.gitignore": "*.pyc\n__pycache__/\n.env",
                f"{branch_name}/src/main.py": f"# Main script for {summary}\n\nprint('Hello from {key}')"
            }

            # Add files to the new branch
            for path, content in files.items():
                try:
                    # Check if the file already exists
                    try:
                        repo.get_contents(path, ref=branch_name)
                        print(f"⚠️ File '{path}' already exists in branch '{branch_name}'. Skipping...")
                        continue
                    except Exception:
                        # File does not exist, proceed to create it
                        repo.create_file(
                            path=path,
                            message=f"Add initial structure for {key}",
                            content=content,
                            branch=branch_name
                        )
                        print(f"✅ Added {path} to {branch_name}")
        
                except Exception as e:
                    print(f"❌ Failed to add {path} to {branch_name}: {e}")

        except Exception as e:
            print(f"❌ Failed to create branch {branch_name}: {e}")

if __name__=="__main__":
    main()