import markdown2
import bleach
from typing import List
from bs4 import BeautifulSoup

class MarkdownHelper:
    """Helper class for markdown processing."""
    
    @staticmethod
    def markdown_to_html(content: str, extras: List[str] = None) -> str:
        """Convert markdown to HTML with specified extras."""
        if extras is None:
            extras = ['fenced-code-blocks', 'tables', 'metadata']
            
        return markdown2.markdown(content, extras=extras)
        
    @staticmethod
    def sanitize_html(html_content: str) -> str:
        """Sanitize HTML content for security."""
        allowed_tags = [
            'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'a', 'strong', 'em', 'code', 'pre',
            'ul', 'ol', 'li', 'blockquote', 'img',
            'table', 'thead', 'tbody', 'tr', 'th', 'td'
        ]
        
        allowed_attributes = {
            'a': ['href', 'title'],
            'img': ['src', 'alt', 'title']
        }
        
        return bleach.clean(
            html_content,
            tags=allowed_tags,
            attributes=allowed_attributes,
            strip=True
        )
        
    @staticmethod
    def extract_code_blocks(markdown_content: str) -> List[dict]:
        """Extract code blocks from markdown content."""
        html = markdown2.markdown(
            markdown_content,
            extras=['fenced-code-blocks']
        )
        
        soup = BeautifulSoup(html, 'html.parser')
        code_blocks = []
        
        for pre in soup.find_all('pre'):
            code = pre.find('code')
            if code:
                language = code.get('class', [''])[0].replace('language-', '')
                code_blocks.append({
                    'language': language,
                    'code': code.text
                })
                
        return code_blocks
        
    @staticmethod
    def generate_toc(markdown_content: str) -> List[dict]:
        """Generate table of contents from markdown headers."""
        html = markdown2.markdown(markdown_content)
        soup = BeautifulSoup(html, 'html.parser')
        toc = []
        
        for header in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            level = int(header.name[1])
            text = header.text
            toc.append({
                'level': level,
                'text': text,
                'id': text.lower().replace(' ', '-')
            })
            
        return toc
