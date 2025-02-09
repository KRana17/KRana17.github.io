import pytest
from src.publisher.blog_post import BlogPost
from src.publisher.github_publisher import GitHubBlogPublisher
from src.publisher.blog_generator import BlogGenerator
from datetime import datetime
import os

@pytest.fixture
def sample_post():
    return BlogPost(
        title="Test Post",
        content="This is a test post content",
        tags=["test", "python"],
        author="Test Author",
        description="Test Description"
    )

@pytest.fixture
def github_token():
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        pytest.skip("GITHUB_TOKEN not set")
    return token

def test_blog_post_creation():
    """Test creating a blog post"""
    post = BlogPost(
        title="Test Post",
        content="Test content",
        tags=["test"],
        author="Test Author"
    )
    
    assert post.title == "Test Post"
    assert post.content == "Test content"
    assert "test" in post.tags
    assert post.author == "Test Author"

def test_blog_post_markdown():
    """Test markdown conversion"""
    post = BlogPost(
        title="Test Post",
        content="Test content",
        tags=["test"],
        author="Test Author",
        date=datetime(2025, 1, 1)
    )
    
    markdown = post.to_markdown()
    assert "---" in markdown  # Has frontmatter
    assert "title: Test Post" in markdown
    assert "Test content" in markdown

def test_github_publisher(github_token, sample_post):
    """Test GitHub publisher"""
    publisher = GitHubBlogPublisher(
        repo_name="test-blog",  # Replace with your test repo
        token=github_token
    )
    
    filename = publisher.create_post_filename(sample_post)
    assert filename.endswith('.md')
    assert sample_post.title.lower().replace(' ', '-') in filename

def test_blog_generator():
    """Test blog generator"""
    generator = BlogGenerator()
    
    post_data = {
        'title': 'Test Title',
        'content': 'Test content',
        'description': 'Test description'
    }
    
    post = generator.generate_post(
        template_name='technical-post',
        data=post_data,
        tags=['test'],
        author='Test Author',
        title='Test Title'
    )
    
    assert post.title == 'Test Title'
    assert 'test' in post.tags