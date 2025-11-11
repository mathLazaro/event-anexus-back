from app import db
from models.event_type import EventType
from sqlalchemy import Enum as SqlEnum
from datetime import datetime
from exceptions.business_exceptions import BadRequestException


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    time = db.Column(db.Time, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    capacity = db.Column(db.Integer, nullable=True)
    type = db.Column(SqlEnum(EventType), nullable=False)
    speaker = db.Column(db.String(100), nullable=True)
    institution_organizer = db.Column(db.String(200), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    creator = db.relationship('User', backref=db.backref('events', lazy=True))
    active = db.Column(db.Boolean(), default=True, nullable=False)

    @staticmethod
    def from_dict(data: dict) -> "Event":
        event = Event()

        for field in ['id', 'title', 'description', 'location', 'capacity', 'speaker', 'institution_organizer', 'created_by']:
            if field in data:
                setattr(event, field, data[field])

        if 'type' in data:
            if isinstance(data['type'], EventType):
                event.type = data['type']
            else:
                # Tenta por nome (WORKSHOP) ou por valor (Workshop)
                try:
                    event.type = EventType[data['type'].upper()]
                except KeyError:
                    event.type = EventType(data['type'])
                except KeyError:
                    raise BadRequestException(
                        f"Tipo de evento inválido: {data['type']}")

        if 'date' in data:
            if isinstance(data['date'], datetime):
                event.date = data['date']
            elif isinstance(data['date'], str):
                event.date = datetime.fromisoformat(data['date'])

        if 'time' in data:
            if isinstance(data['time'], str):
                event.time = datetime.strptime(data['time'], "%H:%M").time()
            else:
                event.time = data['time']

        return event

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "date": self.date.isoformat() if self.date else None,
            "time": self.time.strftime("%H:%M") if self.time else None,
            "location": self.location,
            "capacity": self.capacity,
            "type": self.type.value if self.type else None,
            "speaker": self.speaker,
            "institution_organizer": self.institution_organizer,
            "created_by": self.created_by,
        }
