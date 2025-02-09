import pytest
from pathlib import Path
from src.publisher.blog_generator import BlogGenerator
from src.publisher.blog_post import BlogPost

@pytest.fixture
def template_dir(tmp_path):
    """Create a temporary directory with test templates"""
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    
    # Create a test template
    test_template = template_dir / "test-template.md"
    test_template.write_text("""# {{ title }}

{{ description }}

## Introduction
{{ introduction }}

## Content
{{ content }}

*Written by {{ author }}*""")
    
    return template_dir

@pytest.fixture
def generator(template_dir):
    """Create a BlogGenerator instance with test templates"""
    return BlogGenerator(templates_dir=str(template_dir))

def test_generator_initialization(template_dir):
    """Test BlogGenerator initialization"""
    generator = BlogGenerator(templates_dir=str(template_dir))
    assert generator.templates_dir == Path(template_dir)

def test_list_templates(generator, template_dir):
    """Test listing available templates"""
    templates = generator.list_templates()
    assert "test-template" in templates

def test_generate_post(generator):
    """Test generating a blog post from template"""
    post_data = {
        'title': 'Test Post',
        'description': 'Test Description',
        'introduction': 'Test Introduction',
        'content': 'Test Content'
    }
    
    post = generator.generate_post(
        template_name='test-template',
        data=post_data,
        tags=['test'],
        author='Test Author',
        title='Test Post'
    )
    
    assert isinstance(post, BlogPost)
    assert post.title == 'Test Post'
    assert 'Test Description' in post.content
    assert 'Test Introduction' in post.content
    assert 'Test Content' in post.content
    assert 'Written by Test Author' in post.content

def test_invalid_template(generator):
    """Test handling of non-existent template"""
    with pytest.raises(Exception):
        generator.generate_post(
            template_name='non-existent-template',
            data={},
            tags=[],
            author='Test Author'
        )

def test_create_draft(generator, tmp_path):
    """Test creating a draft post"""
    post = BlogPost(
        title="Draft Post",
        content="Draft content",
        tags=["draft"],
        author="Test Author"
    )
    
    drafts_dir = tmp_path / "drafts"
    draft_path = generator.create_draft(post, str(drafts_dir))
    
    assert draft_path.exists()
    assert draft_path.is_file()
    
    # Verify content
    content = draft_path.read_text()
    assert "Draft Post" in content
    assert "Draft content" in content
    assert "Test Author" in content

def test_template_with_missing_variables(generator):
    """Test handling of missing template variables"""
    post_data = {
        'title': 'Test Post',
        # Deliberately missing some variables
    }
    
    post = generator.generate_post(
        template_name='test-template',
        data=post_data,
        tags=['test'],
        author='Test Author',
        title='Test Post'
    )
    
    # The template should handle missing variables gracefully
    assert isinstance(post, BlogPost)
    assert post.title == 'Test Post'