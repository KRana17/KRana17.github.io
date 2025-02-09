import os
import yaml
import datetime
from github import Github
from pathlib import Path
from typing import Dict, List, Optional
import frontmatter
import markdown2

class BlogPost:
    """Represents a blog post with metadata and content."""
    
    def __init__(self, title: str, content: str, tags: List[str], 
                 date: Optional[datetime.datetime] = None):
        self.title = title
        self.content = content
        self.tags = tags
        self.date = date or datetime.datetime.now()
        
    def to_markdown(self) -> str:
        """Convert the blog post to markdown format with frontmatter."""
        metadata = {
            'title': self.title,
            'date': self.date.strftime('%Y-%m-%d'),
            'tags': self.tags
        }
        
        return f"""---
{yaml.dump(metadata)}---

{self.content}
"""

class GitHubBlogPublisher:
    """Handles publishing blog posts to GitHub Pages."""
    
    def __init__(self, repo_name: str, token: str, 
                 branch: str = 'main', posts_dir: str = '_posts'):
        self.github = Github(token)
        self.repo = self.github.get_user().get_repo(repo_name)
        self.branch = branch
        self.posts_dir = posts_dir
        
    def create_post_filename(self, post: BlogPost) -> str:
        """Generate a filename for the blog post."""
        date_prefix = post.date.strftime('%Y-%m-%d')
        # Convert title to URL-friendly slug
        slug = post.title.lower().replace(' ', '-')
        return f"{date_prefix}-{slug}.md"
        
    def publish_post(self, post: BlogPost) -> str:
        """Publish a blog post to GitHub Pages."""
        try:
            # Generate the post content
            content = post.to_markdown()
            
            # Create the file path
            filename = self.create_post_filename(post)
            file_path = f"{self.posts_dir}/{filename}"
            
            # Get the current commit SHA
            ref = self.repo.get_git_ref(f"heads/{self.branch}")
            latest_commit = self.repo.get_git_commit(ref.object.sha)
            
            # Create blob with post content
            blob = self.repo.create_git_blob(content, "utf-8")
            
            # Create tree with the new file
            element = InputGitTreeElement(
                path=file_path,
                mode='100644',
                type='blob',
                sha=blob.sha
            )
            tree = self.repo.create_git_tree([element], base_tree=latest_commit.tree)
            
            # Create commit
            commit = self.repo.create_git_commit(
                message=f"Add blog post: {post.title}",
                tree=tree,
                parents=[latest_commit]
            )
            
            # Update branch reference
            ref.edit(commit.sha)
            
            return f"Successfully published: {filename}"
            
        except Exception as e:
            raise Exception(f"Failed to publish post: {str(e)}")

class BlogGenerator:
    """Generates blog post content from templates and data."""
    
    def __init__(self, templates_dir: str = 'templates'):
        self.templates_dir = Path(templates_dir)
        
    def load_template(self, template_name: str) -> str:
        """Load a blog post template from file."""
        template_path = self.templates_dir / f"{template_name}.md"
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_name}")
            
        with open(template_path, 'r') as f:
            return f.read()
            
    def generate_post(self, template_name: str, 
                     data: Dict[str, str], 
                     tags: List[str]) -> BlogPost:
        """Generate a blog post from a template and data."""
        template = self.load_template(template_name)
        
        # Replace placeholders in template
        content = template
        for key, value in data.items():
            content = content.replace(f"{{${key}}}", value)
            
        return BlogPost(
            title=data.get('title', 'Untitled Post'),
            content=content,
            tags=tags
        )

def main():
    """Example usage of the blog publishing system."""
    # Initialize the publisher with your GitHub token
    token = os.getenv('GITHUB_TOKEN')
    publisher = GitHubBlogPublisher(
        repo_name='dev-blog',
        token=token
    )
    
    # Initialize the blog generator
    generator = BlogGenerator()
    
    # Example data for a blog post
    post_data = {
        'title': 'Understanding Python Decorators',
        'description': 'A deep dive into Python decorators and their use cases',
        'code_example': '''
@timer
def expensive_operation():
    # ... code here
    pass
'''
    }
    
    # Generate and publish the post
    post = generator.generate_post(
        template_name='technical-post',
        data=post_data,
        tags=['python', 'programming', 'decorators']
    )
    
    result = publisher.publish_post(post)
    print(result)

if __name__ == '__main__':
    main()