#!/usr/bin/env python3
import click
import yaml
from pathlib import Path
import sys
from typing import Dict

# Add parent directory to path to import our modules
sys.path.append(str(Path(__file__).parent.parent))

from src.publisher.blog_post import BlogPost
from src.publisher.github_publisher import GitHubBlogPublisher
from src.publisher.blog_generator import BlogGenerator

@click.group()
def cli():
    """CLI tool for managing GitHub blog posts."""
    pass

@cli.command()
@click.option('--template', '-t', help='Template to use', required=True)
@click.option('--config', '-c', help='Configuration file', required=True)
@click.option('--draft', is_flag=True, help='Save as draft instead of publishing')
def create(template: str, config: str, draft: bool):
    """Create a new blog post from template and configuration."""
    try:
        # Load configuration
        with open(config, 'r') as f:
            post_config = yaml.safe_load(f)
            
        # Initialize generator
        generator = BlogGenerator()
        
        # Generate post
        post = generator.generate_post(
            template_name=template,
            data=post_config['data'],
            tags=post_config['tags'],
            author=post_config['author'],
            title=post_config['title'],
            description=post_config.get('description', '')
        )
        
        if