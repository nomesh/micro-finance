#!/usr/bin/env python
import os
import sys

# Apply Django 1.11 Python 3.8+ compatibility patch
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import django_patch

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "microfinance.settings_local")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
