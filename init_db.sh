#!/bin/bash
set -e

echo "=== Running database migrations ==="
python manage_local.py migrate --noinput

echo "=== Creating default superuser ==="
python manage_local.py create_default_superuser

echo "=== Database setup complete ==="
