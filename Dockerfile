FROM python:3.8.18-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip==21.3.1 && \
    pip install --no-cache-dir -r requirements.txt

# Patch Django 1.11 for Python 3.8 compatibility
RUN sed -i "s/'%s=%s' % (k, v) for k, v in params.items(),/('%s=%s' % (k, v) for k, v in params.items()),/" \
    /usr/local/lib/python3.8/site-packages/django/contrib/admin/widgets.py

# Copy application code
COPY . .

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Collect static files
RUN python manage_local.py collectstatic --no-input || true

# Use entrypoint script
ENTRYPOINT ["./entrypoint.sh"]
