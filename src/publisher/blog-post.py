from datetime import datetime
from typing import List, Optional
import yaml

class BlogPost:
    """Represents a blog post with metadata and content."""
    
    def __init__(
        self, 
        title: str, 
        content: str, 
        tags: List[str], 
        author: str,
        date: Optional[datetime] = None,
        description: str = ""
    ):
        self.title = title
        self.content = content
        self.tags = tags
        self.author = author
        self.date = date or datetime.now()
        self.description = description
        
    def to_markdown(self) -> str:
        """Convert the blog post to markdown format with frontmatter."""
        metadata = {
            'title': self.title,
            'date': self.date.strftime('%Y-%m-%d'),
            'tags': self.tags,
            'author': self.author,
            'description': self.description
        }
        
        return f"""---
{yaml.dump(metadata)}---

{self.content}
"""
    
    @classmethod
    def from_markdown(cls, markdown_content: str) -> 'BlogPost':
        """Create a BlogPost instance from markdown content with frontmatter."""
        try:
            # Split frontmatter and content
            _, frontmatter, content = markdown_content.split('---', 2)
            
            # Parse frontmatter
            metadata = yaml.safe_load(frontmatter)
            
            # Parse date
            date = datetime.strptime(metadata['date'], '%Y-%m-%d')
            
            return cls(
                title=metadata['title'],
                content=content.strip(),
                tags=metadata['tags'],
                author=metadata['author'],
                date=date,
                description=metadata.get('description', '')
            )
        except Exception as e:
            raise ValueError(f"Invalid markdown format: {str(e)}")
