from app import db
from datetime import datetime


class Certificate(db.Model):
    __tablename__ = 'certificates'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    certificate_path = db.Column(db.String(500), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)

    user = db.relationship('User', backref=db.backref('certificates', lazy=True))
    event = db.relationship('Event', backref=db.backref('certificates', lazy=True))

    __table_args__ = (
        db.UniqueConstraint('user_id', 'event_id', name='uq_certificate_user_event'),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "event_id": self.event_id,
            "generated_at": self.generated_at.isoformat() if self.generated_at else None,
            "certificate_path": self.certificate_path,
            "event": {
                "title": self.event.title,
                "date": self.event.date.isoformat() if self.event.date else None,
                "location": self.event.location,
                "speaker": self.event.speaker,
                "institution_organizer": self.event.institution_organizer
            } if self.event else None
        }
