from github import Github
from dotenv import load_dotenv
import os
import re

def clean_repo_name(repo_name):
    """Clean repository name by removing URL parts if present."""
    # If it's a URL, extract just the repository name
    url_match = re.search(r'[\/]([^\/]+)\.git$|[\/]([^\/]+)$', repo_name)
    if url_match:
        return next(group for group in url_match.groups() if group is not None)
    return repo_name

def test_github_connection():
    load_dotenv()
    
    # Get and clean up environment variables
    token = os.getenv('GITHUB_TOKEN')
    raw_repo_name = os.getenv('GITHUB_REPO')
    repo_name = clean_repo_name(raw_repo_name)
    
    print(f"\nRepository name analysis:")
    print(f"- Raw name from .env: {raw_repo_name}")
    print(f"- Cleaned name: {repo_name}")
    
    try:
        g = Github(token)
        user = g.get_user()
        print(f"\nAuthentication details:")
        print(f"- Authenticated as: {user.login}")
        
        # First, let's try to find the repository in the user's repositories
        print("\nSearching for repository in your accessible repositories...")
        found_repo = None
        for repo in user.get_repos():
            if repo.name.lower() == repo_name.lower():
                found_repo = repo
                print(f"- Found matching repository: {repo.full_name}")
                break
        
        if found_repo:
            print(f"\nRepository details:")
            print(f"- Full name: {found_repo.full_name}")
            print(f"- URL: {found_repo.html_url}")
            print(f"- Description: {found_repo.description or 'No description'}")
            print(f"- Private: {found_repo.private}")
        else:
            print("\nRepository not found in accessible repositories!")
            print("Available repositories:")
            for repo in user.get_repos():
                print(f"- {repo.full_name}")
        
        # Now try to access it directly
        print(f"\nAttempting direct repository access...")
        direct_repo = user.get_repo(repo_name)
        print(f"- Direct access successful: {direct_repo.full_name}")
        
    except Exception as e:
        print(f"\nError details:")
        print(f"- Error type: {type(e).__name__}")
        print(f"- Error message: {str(e)}")
        print(f"- Attempted repository name: {repo_name}")
        print("\nTroubleshooting steps:")
        print("1. Check your .env file contains exactly:")
        print("   GITHUB_TOKEN=your_token_here")
        print("   GITHUB_REPO=test-blog")
        print("2. Ensure there are no spaces or quotes in the .env file")
        print("3. Verify you have the repository at:")
        print(f"   https://github.com/{user.login}/test-blog")

if __name__ == "__main__":
    test_github_connection()