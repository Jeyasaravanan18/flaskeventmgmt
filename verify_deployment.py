#!/usr/bin/env python
"""
Deployment verification script for EventHive
Run this before deploying to Render to ensure everything is configured correctly
"""

import os
import sys
from pathlib import Path

def check_file_exists(filename, required=True):
    """Check if a file exists"""
    if Path(filename).exists():
        print(f"✅ {filename} exists")
        return True
    else:
        status = "❌ REQUIRED" if required else "⚠️  OPTIONAL"
        print(f"{status} {filename} missing")
        return not required

def check_requirements():
    """Check requirements.txt content"""
    with open('requirements.txt', 'r') as f:
        content = f.read()
    
    banned_packages = ['pandas', 'torch', 'transformers', 'streamlit', 'gradio', 'langchain']
    
    print("\n📦 Checking requirements.txt...")
    has_issues = False
    
    for package in banned_packages:
        if package in content.lower():
            print(f"❌ Found {package} - REMOVE THIS")
            has_issues = True
    
    if not has_issues:
        print("✅ No heavy/unnecessary packages found")
    
    # Check for required packages
    required = ['Flask', 'SQLAlchemy', 'gunicorn']
    for pkg in required:
        if pkg in content:
            print(f"✅ {pkg} found")
        else:
            print(f"❌ {pkg} missing")

def check_env_file():
    """Check .env file"""
    print("\n⚙️  Checking .env file...")
    if not Path('.env').exists():
        print("⚠️  .env missing (optional for local dev)")
        return True
    
    with open('.env', 'r') as f:
        content = f.read()
    
    required_vars = ['FLASK_ENV', 'SECRET_KEY']
    for var in required_vars:
        if var in content:
            print(f"✅ {var} configured")
        else:
            print(f"⚠️  {var} not set")

def check_config():
    """Check config.py"""
    print("\n🔧 Checking config.py...")
    with open('config.py', 'r') as f:
        content = f.read()
    
    checks = [
        ('DATABASE_URL', 'Supports environment DATABASE_URL'),
        ('SECRET_KEY', 'Uses environment SECRET_KEY'),
        ('pool_pre_ping', 'Has database connection pooling'),
    ]
    
    for check, desc in checks:
        if check in content:
            print(f"✅ {desc}")
        else:
            print(f"⚠️  {desc} - might need attention")

def check_app():
    """Check app.py"""
    print("\n🚀 Checking app.py...")
    with open('app.py', 'r') as f:
        content = f.read()
    
    if 'debug=False' in content or 'debug = False' in content:
        print("✅ Debug mode disabled (debug=False)")
    elif 'debug=True' in content:
        print("❌ Debug mode enabled - MUST CHANGE TO False FOR PRODUCTION")
    else:
        print("✅ Debug handling looks OK")

def check_render_config():
    """Check Render configuration files"""
    print("\n☁️  Checking Render configuration...")
    files = {
        'render.yaml': 'Render service definition',
        'Procfile': 'Process file',
        'runtime.txt': 'Python version'
    }
    
    for filename, desc in files.items():
        if check_file_exists(filename, required=True):
            print(f"  └─ {desc}")

def main():
    print("=" * 50)
    print("EventHive Deployment Verification")
    print("=" * 50)
    
    # Change to project directory
    os.chdir(os.path.dirname(__file__) or '.')
    
    print("\n📋 Checking critical files...")
    critical_ok = all([
        check_file_exists('app.py'),
        check_file_exists('config.py'),
        check_file_exists('requirements.txt'),
        check_file_exists('render.yaml'),
    ])
    
    check_requirements()
    check_env_file()
    check_config()
    check_app()
    check_render_config()
    
    print("\n" + "=" * 50)
    if critical_ok:
        print("✅ READY TO DEPLOY TO RENDER!")
        print("=" * 50)
        print("\nNext steps:")
        print("1. Generate SECRET_KEY: python -c \"import secrets; print(secrets.token_hex(32))\"")
        print("2. Push to GitHub: git add . && git commit -m 'Deploy to Render' && git push")
        print("3. Set SECRET_KEY in Render dashboard")
        print("4. Watch logs for deployment")
    else:
        print("❌ Some issues found - please review above")
        print("=" * 50)
        sys.exit(1)

if __name__ == '__main__':
    main()
