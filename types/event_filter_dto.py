
from datetime import datetime
from models.event_type import EventType
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

    @staticmethod
    def from_dict(data: dict) -> "EventFilterDTO":
        event_filter = EventFilterDTO()

        for field in ['title', 'description', 'location', 'speaker', 'institution_organizer', 'created_by', 'q']:
            if field in data:
                setattr(event_filter, field, data[field])

        if 'date_from' in data:
            event_filter.date_from = format_date(data['date_from'])

        if 'date_to' in data:
            event_filter.date_to = format_date(data['date_to'])

        if 'type' in data:
            event_filter.type = format_event_type(data['type'])

        return event_filter
