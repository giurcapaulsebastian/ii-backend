import fastapi
from fastapi import security
from sqlalchemy import orm

from app.core.models import database as _models
from app.core.schemas import (
    user as _user_schema,
)
from app.core.services import (
    database as _database_service,
    user as _user_service,
)

router = fastapi.APIRouter()


@router.post("/users", tags=["users"])
async def create_user(
        user: _user_schema.UserCreate,
        db: orm.Session = fastapi.Depends(_database_service.get_db)
):
    db_user = await _user_service.get_user_by_email(user.email, db)
    if db_user:
        raise fastapi.HTTPException(status_code=400, detail="Email already in use!")

    await _user_service.create_user(user, db)

    return await _user_service.create_token(db.query(_models.User).filter(_models.User.email == user.email).first())


@router.post("/token", tags=["users"])
async def generate_token(
        form_data: security.OAuth2PasswordRequestForm = fastapi.Depends(),
        db: orm.Session = fastapi.Depends(_database_service.get_db)
):
    print(form_data.username)
    print(form_data.password)
    user = await _user_service.authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise fastapi.HTTPException(status_code=401, detail="Invalid Credentials")

    return await _user_service.create_token(user)


@router.get("/users/me", tags=["users"], response_model=_user_schema.User)
async def get_user(user: _user_schema.User = fastapi.Depends(_user_service.get_current_user)):
    return user
