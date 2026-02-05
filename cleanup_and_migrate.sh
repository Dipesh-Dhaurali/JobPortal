#!/bin/bash

# Clear Python cache and run migrations
echo "Cleaning Python cache files..."
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete

echo "Running Django makemigrations..."
python manage.py makemigrations authuser
python manage.py makemigrations candidate
python manage.py makemigrations hr
python manage.py makemigrations admin_portal

echo ""
echo "Running Django migrate..."
python manage.py migrate

echo ""
echo "Done! Your database is ready."
