from flask import Blueprint, render_template, redirect, url_for, flash, current_app, abort
from flask_login import login_required, current_user
from models.models import db, Event,Feedback
from forms import EventForm,FeedbackForm
from datetime import datetime
from utils.decorators import role_required
from utils.qr_utils import generate_qr_code
from utils.decorators import role_required
# Create a Blueprint
events_bp = Blueprint('events', __name__)

# ------------------------- HOMEPAGE -------------------------
@events_bp.route('/')
@events_bp.route('/index')
def index():
    """Renders the homepage with a few upcoming events."""
    events = Event.query.order_by(Event.event_date.asc()).limit(3).all()
    return render_template('index.html', title='Welcome', events=events)


# ------------------------- EVENT LIST -------------------------
@events_bp.route('/events')
def events_list():
    """Renders the full list of events."""
    all_events = Event.query.order_by(Event.event_date.asc()).all()
    return render_template('events_list.html', title='Upcoming Events', events=all_events)


# ------------------------- CREATE EVENT -------------------------
@events_bp.route('/create_event', methods=['GET', 'POST'])
@login_required
@role_required('Admin', 'Organizer')
def create_event():
    """Handles event creation."""
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            description=form.description.data,
            event_date=form.event_date.data,
            location=form.location.data,
            organizer_id=current_user.id
        )
        db.session.add(event)
        db.session.commit()
        flash('Your event has been created!', 'success')
        return redirect(url_for('events.events_list'))
    
    return render_template('create_event.html', title='Create Event', form=form)


# ------------------------- EDIT EVENT -------------------------
@events_bp.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    """Handles editing an existing event."""
    event = Event.query.get_or_404(event_id)
    
    # Security check: Only organizer or admin can edit
    if event.organizer_id != current_user.id and current_user.role != 'Admin':
        flash('You do not have permission to edit this event.', 'danger')
        abort(403)

    form = EventForm(obj=event)  # Pre-fill with existing event data

    if form.validate_on_submit():
        # Update event details
        event.title = form.title.data
        event.description = form.description.data
        event.event_date = form.event_date.data
        event.location = form.location.data
        
        db.session.commit()
        flash('Your event has been updated successfully!', 'success')

        # Redirect to appropriate dashboard
        if current_user.role == 'Admin':
            return redirect(url_for('dashboard.admin_dashboard'))
        else:
            return redirect(url_for('dashboard.organizer_dashboard'))
    
    return render_template('edit_event.html', title='Edit Event', form=form, event=event)


# ------------------------- DELETE EVENT -------------------------
@events_bp.route('/delete_event/<int:event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    """Handles deleting an event."""
    event = Event.query.get_or_404(event_id)

    # Security check: Only organizer or admin can delete
    if event.organizer_id != current_user.id and current_user.role != 'Admin':
        flash('You do not have permission to delete this event.', 'danger')
        abort(403)

    # Remove all registrations (attendees) to avoid foreign key conflicts
    event.attendees = []  
    db.session.commit()

    # Now delete the event
    db.session.delete(event)
    db.session.commit()

    flash('The event has been deleted successfully.', 'success')

    # Redirect to dashboard
    if current_user.role == 'Admin':
        return redirect(url_for('dashboard.admin_dashboard'))
    else:
        return redirect(url_for('dashboard.organizer_dashboard'))


# ------------------------- REGISTER FOR EVENT -------------------------
@events_bp.route('/register/<int:event_id>', methods=['POST'])
@login_required
@role_required('Student')
def register(event_id):
    """Handles event registration for a student."""
    event = Event.query.get_or_404(event_id)

    if current_user.is_registered(event):
        flash('You are already registered for this event.', 'info')
    else:
        current_user.registered_events.append(event)
        db.session.commit()

        # Generate a QR code for event registration
        qr_data = f"user_id:{current_user.id},event_id:{event.id},event_title:{event.title}"
        generate_qr_code(qr_data, current_user.id, event.id, current_app)

        flash('You have successfully registered for the event!', 'success')
    
    return redirect(url_for('events.events_list'))


# ------------------------- UNREGISTER FROM EVENT -------------------------
@events_bp.route('/unregister/<int:event_id>', methods=['POST'])
@login_required
@role_required('Student')
def unregister(event_id):
    """Handles event unregistration for a student."""
    event = Event.query.get_or_404(event_id)

    if not current_user.is_registered(event):
        flash('You are not registered for this event.', 'info')
    else:
        current_user.registered_events.remove(event)
        db.session.commit()
        flash('You have successfully unregistered from the event.', 'success')
    
    return redirect(url_for('events.events_list'))
@events_bp.route('/feedback/<int:event_id>', methods=['GET', 'POST'])
@login_required
@role_required('Student')
def submit_feedback(event_id):
    """Handles feedback submission for an event."""
    event = Event.query.get_or_404(event_id)
    
    # Security checks:
    # 1. Has the event already passed?
    if event.event_date > datetime.now():
        flash('You can only leave feedback for events that have finished.', 'info')
        return redirect(url_for('dashboard.student_dashboard'))
    
    # 2. Was the student registered for this event?
    if not current_user.is_registered(event):
        flash('You must be registered for an event to leave feedback.', 'danger')
        return redirect(url_for('dashboard.student_dashboard'))

    # 3. Has the student already left feedback?
    existing_feedback = Feedback.query.filter_by(user_id=current_user.id, event_id=event.id).first()
    if existing_feedback:
        flash('You have already submitted feedback for this event.', 'info')
        return redirect(url_for('dashboard.student_dashboard'))

    form = FeedbackForm()
    if form.validate_on_submit():
        feedback = Feedback(
            rating=int(form.rating.data),
            comment=form.comment.data,
            user_id=current_user.id,
            event_id=event.id
        )
        db.session.add(feedback)
        db.session.commit()
        flash('Thank you for your feedback!', 'success')
        return redirect(url_for('dashboard.student_dashboard'))

    return render_template('submit_feedback.html', title='Submit Feedback', form=form, event=event)