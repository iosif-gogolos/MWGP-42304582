#!/bin/bash
# filepath: /Users/iosifgogolos/Documents/IU/Projekt-Software-Development/MWGP-42304582/build.sh
set -o errexit

# Update pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate