#!/bin/bash

# Sino AI IELTS Tutor App Deployment Script

# Exit on error
set -e

echo "Starting Sino AI IELTS Tutor App deployment..."

# Ensure virtual environment exists
if [ ! -d "sino_env" ]; then
    echo "Creating virtual environment..."
    python -m venv sino_env
fi

# Activate virtual environment
echo "Activating virtual environment..."
source sino_env/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create media directories if they don't exist
echo "Setting up media directories..."
mkdir -p media/coach_images

# Copy placeholder coach images
echo "Copying placeholder coach images..."
cp placeholders/*.jpg media/coach_images/

# Run migrations
echo "Running database migrations..."
python manage.py makemigrations accounts
python manage.py makemigrations core
python manage.py makemigrations practice
python manage.py migrate

# Create superuser if it doesn't exist
echo "Checking for admin user..."
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sino.settings')
django.setup()
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Admin user created.')
else:
    print('Admin user already exists.')
"

# Load initial data
echo "Loading initial data..."
python initial_data.py

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run test server (for development only)
echo "Starting development server..."
python manage.py runserver 0.0.0.0:8000

echo "Sino AI IELTS Tutor App deployment complete."
echo "Access the app at http://localhost:8000"
echo "Admin login: admin / admin123"
echo "Demo user login: demo_user / demopassword123"