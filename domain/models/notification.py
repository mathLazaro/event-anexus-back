from datetime import datetime
from app import db


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    link = db.Column(db.String(200), nullable=True)

    user = db.relationship('User', backref=db.backref('notifications', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "message": self.message,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "is_read": self.is_read,
            "link": self.link
        }
