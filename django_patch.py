# Fix Django 1.11 compatibility with Python 3.8+
import django.contrib.admin.widgets as admin_widgets

# Patch the problematic line
original_url_params = admin_widgets.url_params_from_lookup_dict

def patched_url_params(d):
    return '&'.join(('%s=%s' % (k, v) for k, v in d.items()))

admin_widgets.url_params_from_lookup_dict = patched_url_params
