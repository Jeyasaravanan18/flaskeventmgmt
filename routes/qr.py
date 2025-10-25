# eventhive/routes/qr.py

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from models.models import db, User, Event,registrations
from utils.decorators import role_required
import json

qr_bp = Blueprint('qr', __name__)

@qr_bp.route('/scan')
@login_required
@role_required('Organizer')
def scan():
    """Renders the QR code scanner page for organizers."""
    return render_template('scan.html', title='Scan QR Code')

@qr_bp.route('/verify_attendance', methods=['POST'])
@login_required
@role_required('Organizer')
def verify_attendance():
    """Verifies the scanned QR code data against the database."""
    try:
        data = request.get_json()
        qr_data_str = data.get('qr_data')
        
        # The QR data is a string like: "user_id:1,event_id:2,event_title:Workshop"
        # We need to parse it to get the user_id and event_id
        parts = qr_data_str.split(',')
        user_id = int(parts[0].split(':')[1])
        event_id = int(parts[1].split(':')[1])

        user = User.query.get(user_id)
        event = Event.query.get(event_id)

        if not user or not event:
            return jsonify({'success': False, 'message': 'Invalid QR Code: User or Event not found.'})

        # Check if the user is actually registered for this event
        if not user.is_registered(event):
            return jsonify({'success': False, 'message': f'{user.username} is not registered for {event.title}.'})
        
        # --- (Future Step): Mark attendance in the database ---
        # For now, we just confirm the registration is valid.
        stmt = db.update(registrations).where(
            registrations.c.user_id == user_id,
            registrations.c.event_id == event_id
        ).values(attended=True)
        
        # Execute the statement and commit
        db.session.execute(stmt)
        db.session.commit()
        return jsonify({
            'success': True, 
            'message': f'Success! Attendance confirmed for {user.username} at {event.title}.'
        })

    except Exception as e:
        return jsonify({'success': False, 'message': f'An error occurred: {str(e)}'})