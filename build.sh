#!/usr/bin/env bash
# Build script for Render deployment
# exit on error
set -o errexit

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Navigating to app directory..."
cd app

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Running database migrations..."
python manage.py migrate

echo "Build completed successfully!"
