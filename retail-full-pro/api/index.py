"""
Vercel entry point — imports the Flask app from the parent directory.
Vercel calls the `app` variable as a WSGI handler.
"""
import sys, os

# Add the project root to the path so we can import app.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app  # noqa: F401  — Vercel picks up `app` automatically
