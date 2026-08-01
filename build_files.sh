#!/bin/bash
echo "Building Vercel Project..."
python3 -m pip install -r requirements.txt --break-system-packages
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput --clear
echo "Build complete."

