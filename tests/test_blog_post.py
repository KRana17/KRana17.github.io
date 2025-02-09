import pytest
from datetime import datetime
from src.publisher.blog_post import BlogPost

# Fixture to create a sample blog post for testing
@pytest.fixture
def sample_post():
    return BlogPost(
        title="Test Blog Post",
        content="This is the content of our test blog post.",
        tags=["python", "testing"],
        author="Test Author",
        description="A test blog post description"
    )

def test_blog_post_initialization():
    """Test that a BlogPost is created with correct attributes"""
    post = BlogPost(
        title="My Test Post",
        content="Test content",
        tags=["test"],
        author="Test Author"
    )
    
    # Verify all attributes are set correctly
    assert post.title == "My Test Post"
    assert post.content == "Test content"
    assert post.tags == ["test"]
    assert post.author == "Test Author"
    assert isinstance(post.date, datetime)

def test_blog_post_markdown_conversion(sample_post):
    """Test that a blog post converts to markdown correctly"""
    markdown = sample_post.to_markdown()
    
    # Check frontmatter format
    assert markdown.startswith('---')
    assert '---' in markdown[3:]  # Check for closing frontmatter
    
    # Check content presence
    assert sample_post.title in markdown
    assert sample_post.content in markdown
    assert all(tag in markdown for tag in sample_post.tags)
    assert sample_post.author in markdown

def test_blog_post_from_markdown():
    """Test creating a BlogPost from markdown content"""
    markdown_content = """---
title: Test Post
date: 2025-01-01
tags:
  - python
  - test
author: Test Author
description: Test Description
---

This is the test content."""

    post = BlogPost.from_markdown(markdown_content)
    
    assert post.title == "Test Post"
    assert post.content.strip() == "This is the test content."
    assert "python" in post.tags
    assert "test" in post.tags
    assert post.author == "Test Author"
    assert post.description == "Test Description"

def test_invalid_markdown():
    """Test handling of invalid markdown"""
    invalid_markdown = """Not a valid frontmatter
This is just content"""
    
    with pytest.raises(ValueError):
        BlogPost.from_markdown(invalid_markdown)

def test_empty_fields():
    """Test blog post creation with minimal fields"""
    post = BlogPost(
        title="Title Only",
        content="Content Only",
        tags=[],
        author="Author Only"
    )
    
    assert post.description == ""  # Optional field should be empty
    assert isinstance(post.date, datetime)  # Date should be auto-generated