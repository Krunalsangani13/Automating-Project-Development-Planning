import streamlit as st
from jira import JIRA
from github import Github
from docx import Document
import re
import os

st.title("Automated Project Management App")

# Jira and Github credentials
JIRA_EMAIL=st.text_input("jira Email",value="krunaltemp1312@gmail.com")
JIRA_API_TOKEN=st.text_input("jira API Token",type="password",value="ATATT3xFfGF0m2hT76p98PamB2UplDmhIXqR9TZzXpXiA7Xy34mmK7FZu2wNAdIBIQmpl_enwBKKLwYRv6Orf7nlLYfGcEnA0hLmP4gi1SbALogo74_Hg6KveA6RQ-id8zsS1zuiAABRbTxzOvdYq5cztG1QGUPjG9q_RNBK3MaDaHwFct5bnQo=6369861D")
JIRA_SERVER=st.text_input("jira Server URL",value="https://krunaltemp1312.atlassian.net")
PROJECT_KEY=st.text_input("Jira Project Key",value="KAN")

GITHUB_TOKEN=st.text_input("GitHub PAT",type="password",value="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")
REPO_NAME=st.text_input("GitHub Repository Name",value="Krunalsangani13/Automating-Project-Development-Planning")

# Section 1: Task 1 - Automating Jira Ticket Creation
st.header("Task 1: Automating Jira Ticket Creation")
docx_file = st.file_uploader("Upload Requirements (.docx)", type=["docx"])
if st.button("Generate Jira Tickets"):
    try:
        if docx_file:
            doc=Document(docx_file)
            requirements=[p.text.strip() for p in doc.paragraphs if p.text.strip()]

            jira_options = {'server': JIRA_SERVER}
            jira = JIRA(options=jira_options, basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN))
      
            for req in requirements:
                issue_dict = {
                    'project': {'key': PROJECT_KEY},
                    'summary': req[:50],  # Use the first 50 characters for summary
                    'description': req,
                    'issuetype': {'name': 'Task'}
                }
                issue=jira.create_issue(fields=issue_dict)
                # st.success(f"Generated Jira Ticket: {issue.key} - {issue.fields.summary}")
                st.success(f"Generated Jira Ticket: {issue.key} - {req[:50]}...")

            st.success("Jira ticket generation complete!")
        else:
             st.warning("Please upload a .docx file to generate tickets.")
    except Exception as e:
        st.error(f"Failed to generate Jira tickets: {e}")

# Section 2: Task 2 - Automating GitHub Repository Creation and Structuring
st.header("Task 2: Automating GitHub Repository Creation and Structuring")
if st.button("Generate GitHub Branches and Files"):
    try:
        # Connect to Jira
        jira_options = {'server': JIRA_SERVER}
        jira = JIRA(options=jira_options, basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN))
        issues = jira.search_issues(f'project={PROJECT_KEY}', maxResults=50) # ✅ Fetch Jira tickets

        # Connect to GitHub
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)

        for issue in issues:
            key = issue.key
            summary = issue.fields.summary.strip()
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
            
            # Create the branch if it doesn't exist
            if branch_name not in [branch.name for branch in repo.get_branches()]:
                main_branch = repo.get_branch("main")
                repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=main_branch.commit.sha)
                st.success(f"Created branch: {branch_name}")
            else:
                st.warning(f"Branch '{branch_name}' already exists. Skipping...")
            
            # Create initial files
            files = {
                f"{branch_name}/README.md": f"# {summary}\n\nDescription for {key} - {summary}",
                f"{branch_name}/.gitignore": "*.pyc\n__pycache__/\n.env",
                f"{branch_name}/src/main.py": f"# Main script for {summary}\n\nprint('Hello from {key}')"
            }
            for path, content in files.items():
                try:
                    repo.get_contents(path, ref=branch_name)
                    st.warning(f"File '{path}' already exists. Skipping...")
                except Exception:
                    repo.create_file(path=path, message=f"Add initial structure for {key}", content=content, branch=branch_name)
                    st.success(f"Added {path} to {branch_name}")
        st.success("Branch and file creation complete!")
    except Exception as e:
        st.error(f"Failed to create branches and files: {e}")

# Section 3: Task 3 - Automating Test Case Creation
st.header("Task 3: Automating Test Case Creation")
if st.button("Generate Test Cases"):
    try:
        # Connect to Jira
        jira_options = {'server': JIRA_SERVER}
        jira = JIRA(options=jira_options, basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN))
        issues = jira.search_issues(f'project={PROJECT_KEY}', maxResults=50)  # ✅ Fetch Jira tickets
        
        # Connect to GitHub
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        
        for issue in issues:
            key = issue.key
            summary = issue.fields.summary.strip()
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

            # Ensure the branch is up-to-date (Git Pull)
            try:
                repo.get_branch(branch_name)
                st.info(f"📥 Pulling latest changes for branch '{branch_name}'...")
                # You can't actually run "git pull" through the API, but you can ensure the latest commit is fetched
                latest_commit = repo.get_branch(branch_name).commit.sha
                st.success(f"✅ Fetched latest commit for '{branch_name}': {latest_commit}")
            except Exception as e:
                st.warning(f"⚠️ Branch '{branch_name}' does not exist. Skipping...")
                continue

            # Generate test case file
            test_file_path = f"{branch_name}/tests/test_{clean_summary}.py"
            test_content = f"""def test_{clean_summary}():\n    # Given: {summary}\n    # When: {issue.fields.description.split('.')[0]}\n    # Then: Add your test logic here\n    assert True  # Replace with actual test logic\n"""
            
            try:
                # Check if the file already exists
                repo.get_contents(test_file_path, ref=branch_name)
                st.warning(f"⚠️ Test file '{test_file_path}' already exists. Skipping...")
            except Exception:
                # Create the test file
                repo.create_file(path=test_file_path, message=f"Add test file for {key}", content=test_content.strip(), branch=branch_name)
                st.success(f"✅ Generated test case: {test_file_path}")

        st.success("Test case generation complete!")
    except Exception as e:
        st.error(f"⚠️ Failed to generate test cases: {e}")