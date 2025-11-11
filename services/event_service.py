from models import Event, EventType, User, event_participants
from app import db
from exceptions import BadRequestException, NotFoundException
from exceptions.business_exceptions import UnauthorizedException
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from utils import parse_integrity_error


def list_events(user) -> list[Event]:
    return Event.query.filter_by(created_by=user.id, active=True).all()


def list_available_events() -> list[dict]:
    """RFS08 - Lista eventos futuros com inscrições abertas"""
    now = datetime.now()
    events = Event.query.filter(
        Event.active == True,
        Event.date >= now
    ).order_by(Event.date.asc()).all()

    result = []
    for event in events:
        enrolled_count = db.session.query(event_participants).filter_by(
            event_id=event.id,
            active=True
        ).count()

        remaining_slots = None
        if event.capacity:
            remaining_slots = event.capacity - enrolled_count

        event_dict = event.to_dict()
        event_dict['remaining_slots'] = remaining_slots

        result.append(event_dict)

    return result


def get_by_id(event_id) -> Event:
    event = Event.query.filter_by(id=event_id, active=True).first()
    if not event:
        raise NotFoundException()
    return event


def get_public_event_details(event_id: int) -> dict:
    event = get_by_id(event_id)

    enrolled_count = db.session.query(event_participants).filter_by(
        event_id=event_id,
        active=True
    ).count()

    remaining_slots = None
    is_full = False

    if event.capacity:
        remaining_slots = event.capacity - enrolled_count
        is_full = remaining_slots <= 0

    event_dict = event.to_dict()
    event_dict['enrolled_count'] = enrolled_count
    event_dict['remaining_slots'] = remaining_slots
    event_dict['is_full'] = is_full
    event_dict['is_past'] = event.date < datetime.now()

    return event_dict


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

    db_event = Event.query.filter_by(id=event_id, active=True).first()
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
    event = Event.query.filter_by(id=event_id, active=True).first()
    if not event:
        raise NotFoundException()

    if event.created_by != user_id:
        raise UnauthorizedException("Você não tem permissão para excluir este evento.")

    event.active = False

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise


def deleteAllByUser(user_id: int) -> None:
    events = Event.query.filter_by(created_by=user_id, active=True).all()
    for event in events:
        event.active = False

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise


def enroll_user(event_id: int, user: User) -> None:
    event = get_by_id(event_id)

    if event.date < datetime.now():
        raise BadRequestException(
            details=[{"event": "Não é possível se inscrever em eventos passados."}])

    existing = db.session.query(event_participants).filter_by(
        event_id=event_id,
        user_id=user.id,
        active=True
    ).first()

    if existing:
        raise BadRequestException(
            details=[{"enrollment": "Você já está inscrito neste evento."}])

    if event.capacity:
        enrolled_count = db.session.query(event_participants).filter_by(
            event_id=event_id,
            active=True
        ).count()

        if enrolled_count >= event.capacity:
            raise BadRequestException(
                details=[{"event": "Este evento está lotado."}])

    try:
        stmt = event_participants.insert().values(
            user_id=user.id,
            event_id=event_id,
            registered_at=datetime.now(),
            active=True
        )
        db.session.execute(stmt)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        raise BadRequestException(details=[parse_integrity_error(e)])
    except Exception as e:
        db.session.rollback()
        raise


def cancel_enrollment(event_id: int, user: User) -> None:
    event = get_by_id(event_id)

    if event.date < datetime.now():
        raise BadRequestException(
            details=[{"event": "Não é possível cancelar inscrição em eventos passados."}])

    enrollment = db.session.query(event_participants).filter_by(
        event_id=event_id,
        user_id=user.id,
        active=True
    ).first()

    if not enrollment:
        raise NotFoundException("Você não está inscrito neste evento.")

    try:
        stmt = event_participants.update().where(
            event_participants.c.event_id == event_id,
            event_participants.c.user_id == user.id
        ).values(active=False)
        db.session.execute(stmt)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise


def list_user_enrollments(user: User) -> list[dict]:
    """Lista eventos nos quais o usuário está inscrito"""
    events = Event.query.join(
        event_participants,
        Event.id == event_participants.c.event_id
    ).filter(
        event_participants.c.user_id == user.id,
        event_participants.c.active == True,
        Event.active == True
    ).order_by(Event.date.asc()).all()

    result = []
    for event in events:
        enrolled_count = db.session.query(event_participants).filter_by(
            event_id=event.id,
            active=True
        ).count()

        remaining_slots = None
        if event.capacity:
            remaining_slots = event.capacity - enrolled_count

        event_dict = event.to_dict()
        event_dict['remaining_slots'] = remaining_slots

        result.append(event_dict)

    return result


def list_event_participants(event_id: int, organizer_id: int) -> list[User]:
    """Lista participantes de um evento (apenas para organizador)"""
    event = get_by_id(event_id)

    if event.created_by != organizer_id:
        raise UnauthorizedException(
            "Você não tem permissão para ver os participantes deste evento.")

    return User.query.join(
        event_participants,
        User.id == event_participants.c.user_id
    ).filter(
        event_participants.c.event_id == event_id,
        event_participants.c.active == True,
        User.active == True
    ).all()


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
