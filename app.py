# eventhive/app.py

from flask import Flask
from config import Config
from models.models import db
from flask_migrate import Migrate
from flask_login import LoginManager

# Create and configure the app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize database and migration engine
db.init_app(app)
migrate = Migrate(app, db)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login' # Redirect to login page if user is not authenticated

# This function is required by Flask-Login to load a user
from models.models import User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Import and register blueprints
from routes.events import events_bp
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
# from routes.dashboard import dashboard_bp # We'll create these later
from routes.qr import qr_bp             

app.register_blueprint(events_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(dashboard_bp)
# app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
app.register_blueprint(qr_bp, url_prefix='/qr')

@app.cli.command("create-admin")
def create_admin():
    """Creates a new admin user."""
    import getpass
    username = input("Enter admin username: ")
    email = input("Enter admin email: ")
    password = getpass.getpass("Enter admin password: ")

    # Check if user already exists
    if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
        print("Error: A user with that email or username already exists.")
        return

    admin = User(username=username, email=email, role='Admin')
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()
    print(f"Admin user {username} created successfully!")
if __name__ == '__main__':
    app.run(debug=True)