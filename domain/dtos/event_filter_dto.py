
import base64
from datetime import datetime
import json
from sqlalchemy.orm import Query
from domain.models import EventType, Event
from utils.format_utils import format_date, format_event_type


class EventFilterDTO:
    title: str = None
    description: str = None
    date_from: datetime = None
    date_to: datetime = None
    location: str = None
    type: EventType = None
    speaker: str = None
    institution_organizer: str = None
    created_by: int = None
    q : str = None  # title | description | location | speaker | institution_organizer
    order_by: str = 'date'
    order_direction: str = 'asc'  # 'asc' | 'desc'

    @staticmethod
    def from_dict(data: str) -> "EventFilterDTO":

        data = base64.b64decode(data).decode('utf-8')
        data = json.loads(data)

        event_filter = EventFilterDTO()

        for field in ['title', 'description', 'location', 'speaker', 'institution_organizer', 'created_by', 'q', 'order_by', 'order_direction']:
            if field in data:
                setattr(event_filter, field, data[field])

        if 'date_from' in data:
            event_filter.date_from = format_date(data['date_from'])

        if 'date_to' in data:
            event_filter.date_to = format_date(data['date_to'])

        if 'type' in data:
            event_filter.type = format_event_type(data['type'])

        return event_filter

    def build_filters(self, query: Query) -> Query:
        q = query if query else Event.query

        if self.title:
            q = q.filter(Event.title.ilike(f"%{self.title}%"))
        if self.description:
            q = q.filter(Event.description.ilike(f"%{self.description}%"))
        if self.date_from:
            q = q.filter(Event.date >= self.date_from)
        if self.date_to:
            q = q.filter(Event.date <= self.date_to)
        if self.location:
            q = q.filter(Event.location.ilike(f"%{self.location}%"))
        if self.type:
            q = q.filter(Event.type == self.type)
        if self.speaker:
            q = q.filter(Event.speaker.ilike(f"%{self.speaker}%"))
        if self.institution_organizer:
            q = q.filter(Event.institution_organizer.ilike(
                f"%{self.institution_organizer}%"))
        if self.created_by:
            q = q.filter(Event.created_by == self.created_by)
        if self.q:
            search = f"%{self.q}%"
            q = q.filter(
                (Event.title.ilike(search))
                | (Event.description.ilike(search))
                | (Event.location.ilike(search))
                | (Event.speaker.ilike(search))
                | (Event.institution_organizer.ilike(search))
            )

        if self.order_by in ['title', 'description', 'date', 'capacity', 'location', 'type', 'speaker', 'institution_organizer']:
            order_column = getattr(Event, self.order_by)
            if self.order_direction == 'asc':
                q = q.order_by(order_column.asc())
            else:
                q = q.order_by(order_column.desc())

        return q
