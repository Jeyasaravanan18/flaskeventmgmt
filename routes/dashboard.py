# eventhive/routes/dashboard.py

from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from utils.decorators import role_required
from models.models import User, Event, db, registrations, Feedback
from sqlalchemy import func
from datetime import datetime

# --------------------------- Blueprint --------------------------- #
dashboard_bp = Blueprint('dashboard', __name__)

# --------------------------- ADMIN DASHBOARD --------------------------- #
@dashboard_bp.route('/admin_dashboard')
@login_required
@role_required('Admin')
def admin_dashboard():
    # Keep existing queries
    users = User.query.all()
    events = Event.query.order_by(Event.date_posted.desc()).all()
    
    # --- THIS IS THE NEW, MORE EXPLICIT QUERY ---
    event_analytics = db.session.query(
        Event.title, 
        func.count(registrations.c.user_id) # Count user IDs from the registration table
    ).select_from(Event).join(
        registrations, 
        registrations.c.event_id == Event.id, # Explicitly state the join
        isouter=True # This makes it a LEFT JOIN (to include events with 0)
    ).group_by(Event.id, Event.title).all()
    
    print(f"DEBUG: Chart data is: {event_analytics}")
    
    # Prepare data for Chart.js
    chart_labels = [event[0] for event in event_analytics]
    chart_data = [event[1] for event in event_analytics]
    # ------------------------------------

    return render_template('admin_dashboard.html', 
                           title='Admin Dashboard', 
                           users=users, 
                           events=events,
                           chart_labels=chart_labels, 
                           chart_data=chart_data)

# --------------------------- ORGANIZER DASHBOARD --------------------------- #
@dashboard_bp.route('/organizer_dashboard')
@login_required
@role_required('Organizer')
def organizer_dashboard():
    """Organizer dashboard displaying events created by the current organizer."""
    events = (
        Event.query.filter_by(organizer_id=current_user.id)
        .order_by(Event.event_date.desc())
        .all()
    )

    # Prepare attendee + feedback data for each event
    event_data = []
    for event in events:
        # Registered attendees
        attendees = (
            db.session.query(User, registrations.c.attended)
            .join(registrations, User.id == registrations.c.user_id)
            .filter(registrations.c.event_id == event.id)
            .all()
        )

        # Feedback for this event
        feedbacks = Feedback.query.filter_by(event_id=event.id).all()

        # Combine all event data
        event_data.append({
            'event': event,
            'attendees': attendees,
            'feedbacks': feedbacks
        })

    return render_template(
        'organizer_dashboard.html',
        title='Organizer Dashboard',
        event_data=event_data
    )

# --------------------------- STUDENT DASHBOARD --------------------------- #
@dashboard_bp.route('/student_dashboard')
@login_required
@role_required('Student')
def student_dashboard():
    """Student dashboard showing registered events."""
    registered_events = current_user.registered_events.order_by(Event.event_date.asc()).all()

    return render_template(
        'student_dashboard.html',
        title='My Dashboard',
        events=registered_events,
        datetime=datetime  # Pass datetime to template for comparisons
    )

# --------------------------- DELETE USER --------------------------- #
@dashboard_bp.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
@role_required('Admin')
def delete_user(user_id):
    """Handles deleting a user."""
    user = User.query.get_or_404(user_id)

    # Prevent deleting self
    if user.id == current_user.id:
        flash('You cannot delete your own account.', 'danger')
        abort(403)

    # Delete associated feedbacks
    Feedback.query.filter_by(user_id=user.id).delete()

    # Remove from registrations
    db.session.query(registrations).filter_by(user_id=user.id).delete()

    # Delete the user
    db.session.delete(user)
    db.session.commit()

    flash(f'User {user.username} has been deleted successfully.', 'success')
    return redirect(url_for('dashboard.admin_dashboard'))
