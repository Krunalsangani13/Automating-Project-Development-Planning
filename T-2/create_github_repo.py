from github import Github

GITHUB_TOKEN="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"
GITHUB_USERNAME="Krunalsangani13"

# connection
g=Github(GITHUB_TOKEN)

def create_github_repo(repo_name,description="Automated repo creation",private=True):
    try:
        user=g.get_user()
        repo=user.create_repo(
            name=repo_name,
            description=description,
            private=private,
            auto_init=True
        )
        print(f"✅ Repository '{repo_name}' created successfully at {repo.clone_url}")
    except Exception as e:
       print(f"❌ Error creating repository: {e}")

#Run the script
if __name__=="__main__":
    repo_name="Automated-Repo-Test"
    create_github_repo(repo_name) 