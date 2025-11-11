from app import db
from datetime import datetime


# Tabela de associação para a relação many-to-many entre Event e User
event_participants = db.Table(
    'event_participants',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False),
    db.Column('event_id', db.Integer, db.ForeignKey('events.id'), nullable=False),
    db.Column('registered_at', db.DateTime, default=datetime.utcnow, nullable=False),
    db.Column('active', db.Boolean(), default=True, nullable=False),
    db.UniqueConstraint('user_id', 'event_id', name='uq_user_event')
)
