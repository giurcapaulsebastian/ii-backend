import fastapi
from sqlalchemy import orm as _orm

from app.core.models import database as _models
from app.core.schemas import user as _user_schema
from app.core.schemas import note as _note_schema


async def _note_selector(user: _user_schema.User, db: _orm.Session, note_id: int):
    note = db.query(_models.Note).filter(_models.Note.user_id == user.id, _models.Note.id == note_id).first()
    return note


async def create_note(user: _user_schema.User, db: _orm.Session, note: _note_schema.NoteCreate):
    note = _models.Note(**note.dict())
    note.user_id = user.id
    db.add(note)
    db.commit()
    db.refresh(note)
    return _note_schema.Note.from_orm(note)


async def get_note(user: _user_schema.User, db: _orm.Session, note_id: int):
    note = await _note_selector(db=db, note_id=note_id, user=user)
    if note is None:
        raise fastapi.HTTPException(status_code=404, detail="User doesn't have a note with that id!")
    return _note_schema.Note.from_orm(note)


async def get_notes(user: _user_schema.User, db: _orm.Session):
    notes = db.query(_models.Note).filter(_models.Note.user_id == user.id).all()
    if notes is None:
        raise fastapi.HTTPException(status_code=404, detail="User doesn't have notes")
    return list(map(_note_schema.Note.from_orm, notes))
