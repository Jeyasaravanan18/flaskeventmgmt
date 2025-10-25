from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user
from forms import LoginForm, RegistrationForm
from models.models import db, User

# Create a Blueprint
auth_bp = Blueprint('auth', __name__)

# --------------------------- LOGIN --------------------------- #
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login."""
    # If user is already logged in, redirect to homepage
    if current_user.is_authenticated:
        return redirect(url_for('events.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # Find the user by email
        user = User.query.filter_by(email=form.email.data).first()
        
        # Verify credentials
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Logged in successfully!', 'success')
            
            # Redirect to the intended page or homepage
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('events.index'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
            
    return render_template('login.html', title='Login', form=form)


# --------------------------- LOGOUT --------------------------- #
@auth_bp.route('/logout')
def logout():
    """Handles user logout."""
    logout_user()
    return redirect(url_for('events.index'))


# --------------------------- REGISTER --------------------------- #
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handles user registration."""
    if current_user.is_authenticated:
        return redirect(url_for('events.index'))
        
    form = RegistrationForm()
    if form.validate_on_submit():
        # ✅ Updated: include the role from the dropdown
        user = User(
            username=form.username.data,
            email=form.email.data,
            role=form.role.data  # Save selected role (Student/Organizer)
        )
        
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        flash('🎉 Registration successful! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('register.html', title='Register', form=form)
