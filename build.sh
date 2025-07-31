#!/usr/bin/env bash
# Build script for Render deployment
# exit on error
set -o errexit

echo "=== Starting build process ==="
echo "Python version: $(python --version)"
echo "Current directory: $(pwd)"
echo "Directory contents: $(ls -la)"

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Navigating to app directory..."
cd app
echo "App directory contents: $(ls -la)"

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Running database migrations..."
python manage.py migrate

echo "Testing Django configuration..."
python manage.py check --deploy

echo "Build completed successfully!"
