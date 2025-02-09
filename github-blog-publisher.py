from dotenv import load_dotenv
import os
import sys
from pathlib import Path

# Import our custom classes for blog publishing
from src.publisher.blog_post import BlogPost
from src.publisher.github_publisher import GitHubBlogPublisher
from src.publisher.blog_generator import BlogGenerator

def verify_environment():
    """
    Verify that all required environment variables and directories exist.
    Returns tuple of (token, repo_name) if successful.
    """
    # Load environment variables from .env file
    load_dotenv()
    
    # Get GitHub token from environment
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        raise ValueError("GITHUB_TOKEN not found in environment variables. "
                       "Please add it to your .env file.")
    
    # Get repository name from environment
    repo_name = os.getenv('GITHUB_REPO')
    if not repo_name:
        raise ValueError("GITHUB_REPO not found in environment variables. "
                       "Please add it to your .env file.")
    
    # Clean repository name (remove URL parts if present)
    if '/' in repo_name:
        repo_name = repo_name.split('/')[-1]
    if '.git' in repo_name:
        repo_name = repo_name.replace('.git', '')
    
    return token, repo_name

def verify_directory_structure():
    """
    Verify that all required directories exist and create them if needed.
    """
    # Define required directories
    required_dirs = [
        'posts/templates',
        '_posts',
        'posts/drafts'
    ]
    
    # Create directories if they don't exist
    for directory in required_dirs:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    # Verify template exists
    template_path = Path('posts/templates/technical-post.md')
    if not template_path.exists():
        raise FileNotFoundError(
            f"Template file not found at {template_path}. "
            "Please create the template file first."
        )

def main():
    """
    Main function to demonstrate the blog publishing system.
    """
    try:
        print("Starting blog publishing process...")
        
        # Step 1: Verify environment and directory structure
        print("Verifying environment and directories...")
        token, repo_name = verify_environment()
        verify_directory_structure()
        
        # Step 2: Initialize our components
        print("Initializing publisher and generator...")
        publisher = GitHubBlogPublisher(
            repo_name=repo_name,
            token=token
        )
        
        generator = BlogGenerator(templates_dir='posts/templates')
        
        # Step 3: Prepare blog post data
        # Note: Using raw string (r) prefix to handle special characters
        print("Preparing blog post data...")
        code_example = r"""
@timer
def expensive_operation():
    # Example operation
    time.sleep(2)
    return \"Operation completed\"
"""
        
        post_data = {
            "title": "Understanding Python Decorators",
            "language": "python",
            "code_example": code_example.strip(),
            "description": "A deep dive into Python decorators",
            "introduction": "Decorators are a powerful feature in Python that allows you to modify function behavior.",
            "explanation": "When you use a decorator, you are essentially wrapping one function with another.",
            "conclusion": "Decorators provide a clean and reusable way to modify function behavior."
        }
        
        # Step 4: Generate the post
        print("Generating blog post from template...")
        post = generator.generate_post(
            template_name='technical-post',
            data=post_data,
            tags=['python', 'programming', 'decorators'],
            author='Your Name',
            title=post_data['title'],
            description=post_data['description']
        )
        
        # Step 5: Publish the post
        print("Publishing post to GitHub...")
        result = publisher.publish_post(post)
        print(f"Success! {result}")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nTroubleshooting steps:")
        print("1. Check your .env file contains:")
        print("   GITHUB_TOKEN=your_token_here")
        print("   GITHUB_REPO=test-blog")
        print("2. Ensure all required directories exist:")
        print("   - posts/templates/")
        print("   - _posts/")
        print("3. Verify your GitHub token has repository access")
        sys.exit(1)

if __name__ == '__main__':
    main()