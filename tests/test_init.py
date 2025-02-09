"""
Test suite for the GitHub Blog Publisher.

This package contains all tests for the blog publishing system, including:
- BlogPost tests
- GitHubPublisher tests
- BlogGenerator tests

To run the tests, use pytest from the project root directory:
    pytest tests/
"""

import os
import sys

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)