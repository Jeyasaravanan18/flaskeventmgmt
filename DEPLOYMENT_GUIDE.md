# EventHive - Render Deployment Guide

## What Was Fixed

### 1. **Requirements.txt - MAJOR FIX** ✅
**Issue:** Your requirements.txt had 100+ packages including pandas, torch, transformers, streamlit, and many others not needed for a Flask app. These caused compilation failures on Render.

**Fix:** Cleaned down to 12 essential packages:
- Flask framework (Flask, Flask-SQLAlchemy, Flask-Login, Flask-Migrate, Flask-WTF)
- Database (SQLAlchemy)
- Configuration (python-dotenv)
- Features (qrcode, Pillow, email-validator)
- Production server (gunicorn, Werkzeug)

### 2. **Render Configuration** ✅
**Updated render.yaml** with:
- Python 3.11 runtime specification
- Proper gunicorn command with workers, timeout, and port binding
- Production environment variables

### 3. **App Configuration** ✅
**Updated config.py** with:
- Proper PostgreSQL connection string handling (postgres:// → postgresql://)
- Connection pooling for production
- Environment-based database selection

### 4. **Environment Files** ✅
**Created/Updated:**
- `.env` - Local environment variables
- `runtime.txt` - Python version for Render
- `.gitignore` - Prevents committing sensitive files
- `wsgi.py` - Production WSGI entry point
- `Procfile` - Backup process definition

### 5. **Gunicorn Configuration** ✅
Configured with:
- 2 workers for scalability
- Sync worker class (stable for Flask)
- 60-second timeout
- Proper port binding for Render

## Files Changed/Created

1. ✅ **requirements.txt** - Cleaned from 100+ to 12 packages
2. ✅ **render.yaml** - Updated with production config
3. ✅ **config.py** - Enhanced for production database handling
4. ✅ **.env** - Updated for production settings
5. ✅ **Procfile** - Created for production
6. ✅ **runtime.txt** - Created (Python 3.11.4)
7. ✅ **.gitignore** - Created to exclude unnecessary files
8. ✅ **wsgi.py** - Created for WSGI compatibility
9. ✅ **app.py** - Already had debug=False

## How to Deploy to Render

### Step 1: Prepare Your Local Repository
```bash
# Navigate to your project directory
cd C:\Users\rsury\OneDrive\Desktop\eventhive\eventhive

# Check what files will be committed (should exclude __pycache__, app.db, etc.)
git status

# Add all changes
git add .

# Commit changes
git commit -m "Optimize for Render deployment: clean requirements, add production config"

# Push to GitHub
git push origin main
```

### Step 2: Set Up on Render Dashboard

1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name:** eventhive-app
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn --workers 2 --worker-class sync --timeout 60 --bind 0.0.0.0:$PORT app:app`

### Step 3: Set Environment Variables

In Render Dashboard → Service Settings → Environment:

```
SECRET_KEY=generate-a-random-secure-key-here
FLASK_ENV=production
```

**To generate a secure SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Step 4: Deploy

1. Click "Create Web Service"
2. Render will automatically:
   - Clone your repository
   - Install dependencies from requirements.txt
   - Start the application with gunicorn
3. Watch the logs to ensure successful deployment

## Testing Deployment

Once deployed:

1. **Test the main page:**
   ```
   https://your-service-name.onrender.com/
   ```

2. **Check logs in Render:**
   - Dashboard → Your Service → Logs tab
   - Look for "Listening on" message

3. **Common issues to check:**
   - Database initialization errors
   - Missing environment variables
   - Import errors

## Environment Variables Needed in Render

| Variable | Value | Notes |
|----------|-------|-------|
| `SECRET_KEY` | Random string | Use `secrets.token_hex(32)` to generate |
| `FLASK_ENV` | production | Critical for disabling debug mode |
| `DATABASE_URL` | (optional) | Leave empty to use SQLite, or add PostgreSQL URL |

## Local Testing Before Deployment

Before pushing to Render, test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Test the app locally
python app.py

# Test with gunicorn (same as Render will use)
gunicorn --workers 2 --worker-class sync --timeout 60 app:app
```

## Troubleshooting

### Build Fails
- **Error:** `error: metadata-generation-failed`
- **Cause:** Heavy dependencies (pandas, torch, etc.)
- **Fix:** Already done - using cleaned requirements.txt

### Module Not Found
- **Error:** `ModuleNotFoundError: No module named 'X'`
- **Cause:** Missing from requirements.txt
- **Fix:** Add to requirements.txt, push again

### Database Connection Error
- **Error:** `OperationalError: database is locked` or similar
- **Cause:** SQLite issues or wrong DATABASE_URL
- **Fix:** Use PostgreSQL on Render for production

### App Crashes After Deploy
- **Error:** 503 Service Unavailable
- **Cause:** debug=True or gunicorn timeout
- **Fix:** Already set debug=False and increased timeout

### Port Already in Use
- **Error:** `Address already in use`
- **Cause:** Wrong port configuration
- **Fix:** Gunicorn command already handles $PORT variable

## Production Best Practices Implemented

✅ **Debug disabled** - debug=False in production
✅ **Secret key management** - Uses environment variables
✅ **Database pooling** - Configured with pool_pre_ping and pool_recycle
✅ **Gunicorn workers** - 2 workers for concurrency
✅ **Timeout handling** - 60-second timeout to prevent hangs
✅ **Port binding** - Proper 0.0.0.0:$PORT binding for Render
✅ **Dependencies cleaned** - Only essential packages

## After Successful Deployment

1. **Monitor logs** - Check Render dashboard logs regularly
2. **Test features** - Create test user, event, registration
3. **Check QR code generation** - Verify Pillow/QR code functionality
4. **Test forms** - Verify Flask-WTF CSRF protection works

## Rollback if Issues Occur

If deployment fails:
1. Check Render logs for specific errors
2. Fix the issue locally
3. Commit and push to GitHub
4. Render will auto-redeploy

## Need to Scale Later?

On Render, you can:
- Increase number of gunicorn workers
- Add more instances
- Upgrade to PostgreSQL
- Add environment-specific configurations

---

## Summary

Your app is now production-ready for Render! The main issue was bloated requirements.txt. Now you have:
- ✅ Minimal, optimized dependencies
- ✅ Production-grade configuration
- ✅ Proper environment variable handling
- ✅ Database connection pooling
- ✅ Correct gunicorn setup

**Ready to deploy!** 🚀
