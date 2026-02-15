import sys
import os

# Add the api directory to the path for Vercel
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import fastapi_app

app = fastapi_app  # Vercel expects 'app' as the entry point
