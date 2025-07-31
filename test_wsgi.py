#!/usr/bin/env python
"""
Test script to verify WSGI application loads correctly
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

try:
    # Import Django
    import django
    print(f"✓ Django imported successfully: {django.VERSION}")

    # Setup Django
    django.setup()
    print("✓ Django setup completed")

    # Import the WSGI application
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    print("✓ WSGI application created successfully")

    # Check database connection
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print(f"✓ Database connection successful: {result}")

    print("🎉 All checks passed! Application should start correctly.")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
