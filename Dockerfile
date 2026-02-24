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

# Copy application code
COPY . .

# Collect static files
RUN python manage_local.py collectstatic --no-input || true

# Run migrations and start server
CMD python manage_local.py migrate && \
    gunicorn microfinance.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2 --timeout 120
