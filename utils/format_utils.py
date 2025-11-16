from datetime import datetime
from tkinter import EventType
from exceptions.business_exceptions import BadRequestException


def format_date(date):
    if isinstance(date, datetime):
        return date
    elif isinstance(date, str):
        try:
            return datetime.fromisoformat(date)
        except (ValueError, TypeError) as e:
            raise BadRequestException(
                details=[{"date": "Formato de data inválido. Use o formato ISO: YYYY-MM-DDTHH:MM:SS"}])
    else:
        raise BadRequestException(
            details=[{"date": "Data deve ser uma string no formato ISO ou objeto datetime"}])


def format_hour(time):
    if isinstance(time, str):
        try:
            return datetime.strptime(time, "%H:%M").time()
        except ValueError:
            raise BadRequestException(
                details=[{"time": "Formato de hora inválido. Use o formato HH:MM (ex: 14:30)"}])
    else:
        return time


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
