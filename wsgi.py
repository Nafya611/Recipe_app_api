#!/usr/bin/env python
"""
WSGI config for Recipe API deployment.
This file is used by WSGI-compatible web servers to serve your project.
"""

import os
import sys
from pathlib import Path

# Add the app directory to Python path
BASE_DIR = Path(__file__).resolve().parent
app_dir = BASE_DIR / 'app'
sys.path.insert(0, str(app_dir))

# Change to the app directory
os.chdir(str(app_dir))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

# Import the Django WSGI application
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
