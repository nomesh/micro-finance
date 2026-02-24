# Render Deployment Guide

## Prerequisites
1. GitHub account
2. Render account (sign up at https://render.com)

## Deployment Steps

### 1. Push Code to GitHub
```bash
cd /mnt/d/microfinance/micro-finance
git init
git add .
git commit -m "Initial commit for Render deployment"
git branch -M main
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

### 2. Deploy on Render

#### Option A: Using Blueprint (Recommended)
1. Go to https://dashboard.render.com
2. Click "New" → "Blueprint"
3. Connect your GitHub repository
4. Render will automatically detect `render.yaml`
5. Click "Apply" to deploy

#### Option B: Manual Setup
1. Go to https://dashboard.render.com
2. Click "New" → "PostgreSQL"
   - Name: microfinance-db
   - Database: microfinance
   - User: microfinance
   - Click "Create Database"

3. Click "New" → "Web Service"
   - Connect your GitHub repository
   - Name: microfinance-app
   - Runtime: Python 3
   - Build Command: `./build.sh`
   - Start Command: `gunicorn microfinance.wsgi:application`

4. Add Environment Variables:
   - `PYTHON_VERSION` = `3.8.10`
   - `SECRET_KEY` = (generate a random string)
   - `DEBUG` = `False`
   - `DATABASE_URL` = (copy from PostgreSQL service)

5. Click "Create Web Service"

### 3. Create Superuser (After First Deployment)

1. Go to your web service dashboard
2. Click "Shell" tab
3. Run:
```bash
python manage_local.py createsuperuser
```

Or use the Render shell:
```bash
python manage_local.py shell
```
Then:
```python
from micro_admin.models import User
User.objects.create_superuser('admin', 'admin123')
```

### 4. Access Your Application

Your app will be available at: `https://microfinance-app.onrender.com`

## Important Notes

- **Free tier limitations**: App may spin down after 15 minutes of inactivity
- **Database**: PostgreSQL free tier has 90-day retention
- **Celery**: Background tasks won't work on free tier (requires separate worker service)

## Troubleshooting

### Build fails
- Check build logs in Render dashboard
- Ensure all dependencies in requirements.txt are compatible

### Database connection error
- Verify DATABASE_URL is correctly set
- Check PostgreSQL service is running

### Static files not loading
- Ensure `collectstatic` runs in build command
- Check STATIC_ROOT and STATICFILES_STORAGE settings

## Generate Secret Key

Run locally:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
