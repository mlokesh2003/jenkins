import requests
from requests.auth import HTTPBasicAuth

# -----------------------------
# CONFIGURATION
# -----------------------------
USERNAME = "your_username"
APP_PASSWORD = "your_app_password"
WORKSPACE = "your_workspace"

BASE_URL = "https://api.bitbucket.org/2.0"

auth = HTTPBasicAuth(USERNAME, APP_PASSWORD)

# -----------------------------
# LIST REPOSITORIES
# -----------------------------
def list_repositories():
    url = f"{BASE_URL}/repositories/{WORKSPACE}"
    response = requests.get(url, auth=auth)

    if response.status_code == 200:
        repos = response.json()["values"]
        print("\n📦 Repositories:")
        for repo in repos:
            print(f"- {repo['name']} ({repo['slug']})")
    else:
        print("❌ Error fetching repositories:", response.text)

# -----------------------------
# CREATE REPOSITORY
# -----------------------------
def create_repository(repo_name):
    url = f"{BASE_URL}/repositories/{WORKSPACE}/{repo_name}"

    data = {
        "scm": "git",
        "is_private": True,
        "project": {
            "key": "TEST"
        }
    }

    response = requests.post(url, json=data, auth=auth)

    if response.status_code in [200, 201]:
        print(f"✅ Repository '{repo_name}' created successfully!")
    else:
        print("❌ Error creating repo:", response.text)

# -----------------------------
# LIST BRANCHES
# -----------------------------
def list_branches(repo_slug):
    url = f"{BASE_URL}/repositories/{WORKSPACE}/{repo_slug}/refs/branches"
    response = requests.get(url, auth=auth)

    if response.status_code == 200:
        branches = response.json()["values"]
        print("\n🌿 Branches:")
        for branch in branches:
            print(f"- {branch['name']}")
    else:
        print("❌ Error fetching branches:", response.text)

# -----------------------------
# CREATE BRANCH
# -----------------------------
def create_branch(repo_slug, new_branch, source_branch="main"):
    url = f"{BASE_URL}/repositories/{WORKSPACE}/{repo_slug}/refs/branches"

    data = {
        "name": new_branch,
        "target": {
            "hash": get_branch_hash(repo_slug, source_branch)
        }
    }

    response = requests.post(url, json=data, auth=auth)

    if response.status_code in [200, 201]:
        print(f"✅ Branch '{new_branch}' created from '{source_branch}'")
    else:
        print("❌ Error creating branch:", response.text)

def get_branch_hash(repo_slug, branch_name):
    url = f"{BASE_URL}/repositories/{WORKSPACE}/{repo_slug}/refs/branches/{branch_name}"
    response = requests.get(url, auth=auth)

    if response.status_code == 200:
        return response.json()["target"]["hash"]
    else:
        print("❌ Error getting branch hash")
        return None

# -----------------------------
# GET COMMITS
# -----------------------------
def get_commits(repo_slug):
    url = f"{BASE_URL}/repositories/{WORKSPACE}/{repo_slug}/commits"
    response = requests.get(url, auth=auth)

    if response.status_code == 200:
        commits = response.json()["values"]
        print("\n📝 Recent Commits:")
        for commit in commits[:5]:
            print(f"- {commit['message']} ({commit['hash'][:7]})")
    else:
        print("❌ Error fetching commits:", response.text)

# -----------------------------
# MENU
# -----------------------------
def menu():
    while True:
        print("""
========= Bitbucket Automation Tool =========
1. List Repositories
2. Create Repository
3. List Branches
4. Create Branch
5. Get Commits
6. Exit
============================================
""")

        choice = input("Enter your choice: ")

        if choice == "1":
            list_repositories()

        elif choice == "2":
            repo_name = input("Enter repo name: ")
            create_repository(repo_name)

        elif choice == "3":
            repo_slug = input("Enter repo slug: ")
            list_branches(repo_slug)

        elif choice == "4":
            repo_slug = input("Enter repo slug: ")
            new_branch = input("New branch name: ")
            source_branch = input("Source branch (default main): ") or "main"
            create_branch(repo_slug, new_branch, source_branch)

        elif choice == "5":
            repo_slug = input("Enter repo slug: ")
            get_commits(repo_slug)

        elif choice == "6":
            print("👋 Exiting...")
            break

        else:
            print("❌ Invalid choice")

# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    menu()
