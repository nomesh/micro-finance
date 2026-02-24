#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage_local.py collectstatic --no-input
python manage_local.py migrate
