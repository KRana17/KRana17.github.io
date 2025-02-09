from github import Github
from github.InputGitTreeElement import InputGitTreeElement
from typing import Optional
import os
from datetime import datetime
from .blog_post import BlogPost

class GitHubBlogPublisher:
    """Handles publishing blog posts to GitHub Pages."""
    
    def __init__(
        self, 
        repo_name: str, 
        token: Optional[str] = None,
        branch: str = 'main',
        posts_dir: str = '_posts'
    ):
        self.token = token or os.getenv('GITHUB_TOKEN')
        if not self.token:
            raise ValueError("GitHub token is required")
            
        self.github = Github(self.token)
        self.repo = self.github.get_user().get_repo(repo_name)
        self.branch = branch
        self.posts_dir = posts_dir
        
    def create_post_filename(self, post: BlogPost) -> str:
        """Generate a filename for the blog post."""
        date_prefix = post.date.strftime('%Y-%m-%d')
        # Convert title to URL-friendly slug
        slug = '-'.join(
            ''.join(c if c.isalnum() else ' ' for c in post.title.lower()).split()
        )
        return f"{date_prefix}-{slug}.md"
        
    def publish_post(self, post: BlogPost) -> str:
        """Publish a blog post to GitHub Pages."""
        try:
            # Generate the post content
            content = post.to_markdown()
            
            # Create the file path
            filename = self.create_post_filename(post)
            file_path = f"{self.posts_dir}/{filename}"
            
            # Check if file already exists
            try:
                existing_file = self.repo.get_contents(file_path, ref=self.branch)
                # Update existing file
                self.repo.update_file(
                    file_path,
                    f"Update blog post: {post.title}",
                    content,
                    existing_file.sha,
                    branch=self.branch
                )
                return f"Updated: {filename}"
            except Exception:
                # File doesn't exist, create new
                self.repo.create_file(
                    file_path,
                    f"Add blog post: {post.title}",
                    content,
                    branch=self.branch
                )
                return f"Created: {filename}"
            
        except Exception as e:
            raise Exception(f"Failed to publish post: {str(e)}")
            
    def list_posts(self) -> list:
        """List all published blog posts."""
        try:
            contents = self.repo.get_contents(self.posts_dir, ref=self.branch)
            return [content.path for content in contents if content.path.endswith('.md')]
        except Exception as e:
            raise Exception(f"Failed to list posts: {str(e)}")
            
    def delete_post(self, filename: str) -> bool:
        """Delete a blog post."""
        try:
            file_path = f"{self.posts_dir}/{filename}"
            file = self.repo.get_contents(file_path, ref=self.branch)
            self.repo.delete_file(
                file_path,
                f"Delete blog post: {filename}",
                file.sha,
                branch=self.branch
            )
            return True
        except Exception as e:
            raise Exception(f"Failed to delete post: {str(e)}")
