# Create a test.py file in your project root
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Print the token (first few characters)
token = os.getenv('GITHUB_TOKEN')
if token:
    print(f"Token found: {token[:4]}...")
else:
    print("No token found!")