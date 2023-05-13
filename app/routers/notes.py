from typing import List

import fastapi
from sqlalchemy import orm

from app.core.schemas import (
    user as _user_schema,
    note as _note_schema
)
from app.core.services import (
    database as _database_service,
    user as _user_service,
    note as _note_service
)

router = fastapi.APIRouter()


@router.post("/create_note", tags=["notes"], response_model=_note_schema.Note)
async def create_note(
        note: _note_schema.NoteCreate,
        user: _user_schema.User = fastapi.Depends(_user_service.get_current_user),
        db: orm.Session = fastapi.Depends(_database_service.get_db)
):
    return await _note_service.create_note(user=user, db=db, note=note)


# @router.delete("delete_note/{note_id}", tags=["notes"], status_code=204)
# async def delete_note(
#         note_id: int,
#         user: _user_schema.User = fastapi.Depends(_user_service.get_current_user),
#         db: orm.Session = fastapi.Depends(_database_service.get_db)
# ):
#     await _note_service.delete_note(user=user, db=db, note_id=note_id)
#     return {"message": f"Successfully deleted note with id:{note_id}"}
#
#
# @router.put("/update_note/{note_id}", tags=["notes"], status_code=200)
# async def update_note(
#         note_id: int,
#         note: _note_schema.NoteCreate,
#         user: _user_schema.User = fastapi.Depends(_user_service.get_current_user),
#         db: orm.Session = fastapi.Depends(_database_service.get_db)
# ):
#     return await _note_service.update_note(
#         note_id=note_id,
#         note=note,
#         user=user,
#         db=db
#     )


@router.post("/get_note/{note_id}", tags=["notes"], response_model=_note_schema.Note)
async def get_note(
        note_id: int,
        user: _user_schema.User = fastapi.Depends(_user_service.get_current_user),
        db: orm.Session = fastapi.Depends(_database_service.get_db)
):
    return await _note_service.get_note(user=user, db=db, note_id=note_id)


@router.post("/notes", tags=["notes"], response_model=List[_note_schema.Note])
async def get_notes(
        user: _user_schema.User = fastapi.Depends(_user_service.get_current_user),
        db: orm.Session = fastapi.Depends(_database_service.get_db)
):
    return await _note_service.get_notes(user=user, db=db)
