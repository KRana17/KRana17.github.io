from pathlib import Path
from typing import Dict, List
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from .blog_post import BlogPost

class BlogGenerator:
    """Generates blog post content from templates."""
    
    def __init__(self, templates_dir: str = 'templates'):
        self.templates_dir = Path(templates_dir)
        self.env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
    def list_templates(self) -> List[str]:
        """List available templates."""
        return [
            template.stem 
            for template in self.templates_dir.glob('*.md')
        ]
        
    def generate_post(
        self,
        template_name: str,
        data: Dict[str, str],
        tags: List[str],
        author: str,
        title: str = "",
        description: str = ""
    ) -> BlogPost:
        """Generate a blog post from a template and data."""
        try:
            template = self.env.get_template(f"{template_name}.md")
            
            # Generate content from template
            content = template.render(**data)
            
            # Create blog post
            return BlogPost(
                title=title or data.get('title', 'Untitled Post'),
                content=content,
                tags=tags,
                author=author,
                description=description,
                date=datetime.now()
            )
            
        except Exception as e:
            raise Exception(f"Failed to generate post: {str(e)}")
            
    def create_draft(
        self,
        post: BlogPost,
        drafts_dir: str = 'posts/drafts'
    ) -> Path:
        """Save a draft of the blog post."""
        try:
            drafts_path = Path(drafts_dir)
            drafts_path.mkdir(parents=True, exist_ok=True)
            
            # Create filename
            filename = f"draft-{post.date.strftime('%Y%m%d')}-{post.title.lower().replace(' ', '-')}.md"
            file_path = drafts_path / filename
            
            # Save draft
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(post.to_markdown())
                
            return file_path
            
        except Exception as e:
            raise Exception(f"Failed to save draft: {str(e)}")
