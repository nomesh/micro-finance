#!/bin/sh
set -e

echo "=== Running migrations ==="
python manage_local.py migrate --noinput

echo "=== Creating superuser ==="
python manage_local.py create_default_superuser

echo "=== Starting server ==="
exec gunicorn microfinance.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2 --timeout 120
