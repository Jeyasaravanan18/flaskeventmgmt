# eventhive/models/models.py

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Initialize SQLAlchemy
db = SQLAlchemy()
registrations = db.Table('registrations',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True),
    db.Column('attended', db.Boolean, default=False, nullable=False)
)
# Define the User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='Student', nullable=False) # Roles: Student, Organizer, Admin
    registered_events = db.relationship(
        'Event', secondary=registrations,
        backref=db.backref('attendees', lazy='dynamic'), lazy='dynamic')
    def is_registered(self, event):
        """Check if the user is registered for a specific event."""
        return self.registered_events.filter(
            registrations.c.event_id == event.id).count() > 0
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

# Define the Event model
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    event_date = db.Column(db.DateTime, index=True, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    organizer_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Event {self.title}>'
# eventhive/models/models.py
# ... (keep all existing imports and models)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False) # e.g., 1-5 stars
    comment = db.Column(db.Text, nullable=True)
    date_posted = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    
    # Foreign keys to link feedback to a user and an event
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    
    # Relationships
    author = db.relationship('User')
    event = db.relationship('Event')

    def __repr__(self):
        return f'<Feedback for Event {self.event_id} by User {self.user_id}>'