from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException

from config import DEFAULT_SETTINGS
from security import manager, verify_password
from db import get_db
from db_actions import get_user, create_user
from schemas import UserCreate, UserResponse


auth_router = APIRouter()


@auth_router.post("/auth/register")
def register(user: UserCreate, db=Depends(get_db)):
    if get_user(user.email) is not None:
        raise HTTPException(status_code=400,
                            detail="A user with this email already exists")
    else:
        db_user = create_user(db, user)
        return UserResponse(id=db_user.id,
                            email=db_user.email,
                            name=db_user.name)


@auth_router.post(DEFAULT_SETTINGS.token_url)
def login(data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password

    user = get_user(email)
    if user is None:
        raise InvalidCredentialsException
    elif not verify_password(password, user.password):
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data=dict(sub=user.email)
    )
    return {'access_token': access_token, 'token_type': 'Bearer'}
