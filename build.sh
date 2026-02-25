#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip==21.3.1
pip install -r requirements.txt
python manage_local.py collectstatic --no-input
python manage_local.py migrate
python manage_local.py load_defaults
