from datetime import datetime
from domain.models.event_type import EventType
from exceptions.business_exceptions import BadRequestException


def format_date(date: str, time: str = None) -> datetime:
    if isinstance(date, datetime):
        return date
    elif isinstance(date, str):
        try:
            if time:
                date = date.split("T")[0] + "T" + time
            return datetime.fromisoformat(date)
        except (ValueError, TypeError) as e:
            raise BadRequestException(
                details=[{"date": "Formato de data inválido. Use o formato ISO: YYYY-MM-DDTHH:MM:SS"}])
    else:
        raise BadRequestException(
            details=[{"date": "Data deve ser uma string no formato ISO ou objeto datetime"}])


def format_event_type(event_type):
    if isinstance(event_type, EventType):
        return event_type
    else:
        try:
            return EventType[event_type.upper()]
        except KeyError:
            try:
                return EventType(event_type)
            except (KeyError, ValueError):
                raise BadRequestException(
                    details=[{"type": f"Tipo de evento inválido: {event_type}"}])
