#!/usr/bin/env bash
# Start script with error handling for Render deployment

echo "=== Starting Recipe API ==="
echo "Environment variables:"
echo "  PORT: ${PORT:-'Not set'}"
echo "  DATABASE_URL: ${DATABASE_URL:+'Set'}"
echo "  SECRET_KEY: ${SECRET_KEY:+'Set'}"
echo "  DEBUG: ${DEBUG:-'Not set'}"

echo "Testing WSGI application..."
python test_wsgi.py

if [ $? -eq 0 ]; then
    echo "✓ WSGI test passed, starting gunicorn..."
    exec gunicorn wsgi:application -c gunicorn.conf.py
else
    echo "❌ WSGI test failed, exiting..."
    exit 1
fi
