REM ============================================================
REM EventHive - Render Deployment Commands (Copy & Paste)
REM ============================================================

REM STEP 1: Generate SECRET_KEY
REM Run this in Command Prompt and copy the output
python -c "import secrets; print(secrets.token_hex(32))"

REM You'll get something like this (copy it):
REM a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2


REM ============================================================
REM STEP 2: Optional - Verify Everything Locally
REM Run this to check if everything is configured correctly
REM ============================================================

cd C:\Users\rsury\OneDrive\Desktop\eventhive\eventhive
python verify_deployment.py


REM ============================================================
REM STEP 3: Push to GitHub
REM Copy these commands one by one into Command Prompt
REM ============================================================

cd C:\Users\rsury\OneDrive\Desktop\eventhive\eventhive

git add .

git commit -m "Optimize for Render: clean dependencies and production config"

git push origin main


REM ============================================================
REM STEP 4-7: Use Render Dashboard (Web Interface)
REM ============================================================

REM After pushing to GitHub:
REM 1. Go to https://dashboard.render.com
REM 2. Click "New +" button
REM 3. Select "Web Service"
REM 4. Connect your GitHub repo (select eventhive)
REM 5. Keep build and start commands as-is
REM 6. Click "Create Web Service"
REM 7. In Environment section, add:
REM    - SECRET_KEY = <paste from STEP 1>
REM    - FLASK_ENV = production
REM 8. Click "Create Web Service" again
REM 9. Watch logs for "Listening on" message


REM ============================================================
REM IMPORTANT: Environment Variables for Render
REM ============================================================

REM Copy these into Render Dashboard → Environment:

SECRET_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2
REM ^ Use the value from STEP 1 above

FLASK_ENV=production


REM ============================================================
REM OPTIONAL: Test Locally First
REM ============================================================

REM Install requirements
pip install -r requirements.txt

REM Run Flask locally
python app.py

REM OR test with gunicorn (same as Render will use)
gunicorn --workers 2 --worker-class sync --timeout 60 app:app


REM ============================================================
REM HELPFUL COMMANDS FOR LATER
REM ============================================================

REM Recheck if deployment is ready:
python verify_deployment.py

REM Push new changes after deployment:
git add .
git commit -m "Your commit message"
git push origin main
REM ^ Render auto-redeploys after push

REM View your app logs locally:
cd C:\Users\rsury\OneDrive\Desktop\eventhive\eventhive
python app.py

REM Generate a new SECRET_KEY if needed:
python -c "import secrets; print(secrets.token_hex(32))"


REM ============================================================
REM EXPECTED OUTPUT WHEN DEPLOYMENT SUCCEEDS
REM ============================================================

REM You should see in Render logs:
REM - "Building Docker image"
REM - "Installing Python dependencies"
REM - "Listening on 0.0.0.0:PORT"
REM - Service Status: Live (green dot)

REM Then visit: https://eventhive-app.onrender.com


REM ============================================================
REM COMMON ERRORS & SOLUTIONS
REM ============================================================

REM ERROR: "Build failed"
REM FIX: Check Render logs, usually missing SECRET_KEY

REM ERROR: "ModuleNotFoundError: No module named 'X'"
REM FIX: Add package to requirements.txt and push again

REM ERROR: "503 Service Unavailable"
REM FIX: Check app crashes in logs, verify SECRET_KEY set

REM ERROR: "Cannot connect to database"
REM FIX: Use SQLite first (no DATABASE_URL needed)
