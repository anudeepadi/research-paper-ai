import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bright Data Configuration
BRIGHT_DATA_CONFIG = {
    'username': os.getenv('BRIGHT_DATA_USERNAME'),
    'password': os.getenv('BRIGHT_DATA_PASSWORD'),
    'host': os.getenv('BRIGHT_DATA_HOST', 'brd.superproxy.io:33335')
}

# API Configuration
API_SETTINGS = {
    'title': 'Research Paper AI API',
    'description': 'AI-powered academic research assistant using Bright Data',
    'version': '1.0.0'
}