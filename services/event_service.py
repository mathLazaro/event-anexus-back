from models import Event, EventType, user
from app import db
from exceptions import BadRequestException, NotFoundException
from exceptions.business_exceptions import UnauthorizedException
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from utils import parse_integrity_error


def list_events(user) -> list[Event]:
    return Event.query.filter_by(created_by=user.id).all()


def get_by_id(event_id) -> Event:
    event = Event.query.get(event_id)
    if not event:
        raise NotFoundException()
    return event


def create(event: Event) -> int:

    validate_event_types(event)
    validate_event(event)

    try:
        db.session.add(event)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        raise BadRequestException(details=[parse_integrity_error(e)])
    except Exception as e:
        db.session.rollback()
        raise

    return event.id


def update(event_id, event: Event, user_id: int) -> int:

    db_event = Event.query.get(event_id)
    if not db_event:
        raise NotFoundException()

    if db_event.created_by != user_id:
        raise UnauthorizedException("Você não tem permissão para editar este evento.")

    event.created_by = db_event.created_by

    validate_event_types(event)
    validate_event(event)

    event.id = db_event.id
    event.created_by = db_event.created_by

    try:
        db.session.merge(event)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        raise BadRequestException(details=[parse_integrity_error(e)])
    except Exception as e:
        db.session.rollback()
        raise

    return event.id


def delete(event_id: int, user_id: int) -> None:
    event = Event.query.get(event_id)
    if not event:
        raise NotFoundException()

    # Verifica se o usuário é o criador do evento
    if event.created_by != user_id:
        raise UnauthorizedException("Você não tem permissão para excluir este evento.")

    try:
        db.session.delete(event)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise


def validate_event_types(event: Event) -> None:
    errors = []

    if not isinstance(event.title, str):
        errors.append({"title": "O título do evento deve ser uma string."})

    if event.description is not None and not isinstance(event.description, str):
        errors.append({"description": "A descrição do evento deve ser uma string."})

    if not isinstance(event.date, datetime):
        errors.append({"date": "A data do evento deve ser um datetime válido."})

    if not hasattr(event.time, 'hour'):  # Verifica se é um objeto time
        errors.append({"time": "A hora do evento deve ser um time válido."})

    if not isinstance(event.location, str):
        errors.append({"location": "O local do evento deve ser uma string."})

    if event.capacity is not None and not isinstance(event.capacity, int):
        errors.append(
            {"capacity": "A capacidade do evento deve ser um número inteiro."}
        )

    if event.type is not None and not isinstance(event.type, EventType):
        errors.append({"type": "O tipo do evento é inválido."})

    if event.speaker is not None and not isinstance(event.speaker, str):
        errors.append({"speaker": "O palestrante do evento deve ser uma string."})

    if not isinstance(event.institution_organizer, str):
        errors.append(
            {"institution_organizer": "A instituição organizadora deve ser uma string."})

    if event.created_by is not None and not isinstance(event.created_by, int):
        errors.append({"created_by": "O ID do criador deve ser um número inteiro."})

    if errors:
        raise BadRequestException("Erro de validação de tipo", errors)


def validate_event(event: Event, is_update: bool = False) -> None:
    errors = []

    if event.title is None or event.title.strip() == "":
        errors.append({"title": "O título do evento é obrigatório."})
    elif len(event.title) > 100:
        errors.append(
            {"title": "O título do evento deve ter no máximo 100 caracteres."})

    if event.date is None:
        errors.append({"date": "A data do evento é obrigatória."})
    else:
        # Compara apenas a data (sem hora)
        event_date_only = event.date.date() if isinstance(event.date, datetime) else event.date
        today = datetime.now().date()

        if event_date_only < today:
            errors.append({"date": "A data do evento não pode ser no passado."})
        elif event_date_only == today and event.time is not None:
            # Se for hoje, valida se a hora já passou
            if event.time < datetime.now().time():
                errors.append({"time": "A hora do evento não pode ser no passado."})

    if event.time is None:
        errors.append({"time": "A hora do evento é obrigatória."})

    if event.location is None or event.location.strip() == "":
        errors.append({"location": "O local do evento é obrigatório."})
    elif len(event.location) > 200:
        errors.append(
            {"location": "O local do evento deve ter no máximo 200 caracteres."})

    if event.capacity is not None and event.capacity <= 0:
        errors.append({"capacity": "A capacidade do evento deve ser maior que zero."})

    if event.type is None:
        errors.append({"type": "O tipo do evento é obrigatório."})

    if event.institution_organizer is None or event.institution_organizer.strip() == "":
        errors.append(
            {"institution_organizer": "A instituição organizadora é obrigatória."})
    elif len(event.institution_organizer) > 200:
        errors.append(
            {"institution_organizer": "A instituição organizadora deve ter no máximo 200 caracteres."})

    if event.speaker is not None and len(event.speaker) > 100:
        errors.append(
            {"speaker": "O nome do palestrante deve ter no máximo 100 caracteres."})

    if event.created_by is None and not is_update:
        errors.append({"created_by": "O criador do evento é obrigatório."})

    if errors:
        raise BadRequestException("Erro de validação", errors)
