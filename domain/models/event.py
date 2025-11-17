from app import db
from domain.models.event_type import EventType
from domain.models.event_participant import event_participants
from sqlalchemy import Enum as SqlEnum
from utils.format_utils import format_date, format_event_type


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    capacity = db.Column(db.Integer, nullable=True)
    type = db.Column(SqlEnum(EventType), nullable=False)
    speaker = db.Column(db.String(100), nullable=True)
    institution_organizer = db.Column(db.String(200), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    creator = db.relationship('User', foreign_keys=[
                              created_by], backref=db.backref('created_events', lazy=True))

    participants = db.relationship(
        'User',
        secondary=event_participants,
        backref=db.backref('enrolled_events', lazy='dynamic'),
        lazy='dynamic'
    )

    active = db.Column(db.Boolean(), default=True, nullable=False)

    @staticmethod
    def from_dict(data: dict) -> "Event":
        event = Event()

        for field in ['id', 'title', 'description', 'location', 'capacity', 'speaker', 'institution_organizer', 'created_by']:
            if field in data:
                setattr(event, field, data[field])

        if 'type' in data:
            event.type = format_event_type(data['type'])

        if 'date' in data:
            event.date = format_date(data['date'], data.get('time'))

        return event

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "date": self.date.isoformat() if self.date else None,
            "time": self.date.strftime("%H:%M") if self.date else None,
            "location": self.location,
            "capacity": self.capacity,
            "type": self.type.value if self.type else None,
            "speaker": self.speaker,
            "institution_organizer": self.institution_organizer,
            "created_by": self.created_by,
        }
