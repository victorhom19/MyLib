import smtplib
import uuid
from email.message import EmailMessage

from fastapi import Depends, HTTPException, status, Form, Response, Cookie
from fastapi_users import FastAPIUsers
from pydantic import BaseModel
from redis import StrictRedis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.annotation import Annotated
from sqlalchemy.sql.functions import current_user

from auth.auth import auth_backend
from auth.database import get_async_session
from auth.manager import get_user_manager
from auth.schemas import UserCreate, UserRead
from cache.cache import get_cache_instance
from config import MAIL_SERVICE_EMAIL, MAIL_SERVICE_PASS, MAIL_SERVICE_TOKEN_EXPIRATION_TIME
from models.models import User

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

auth_router = fastapi_users.get_auth_router(auth_backend)

register_router = fastapi_users.get_register_router(UserRead, UserCreate)

reset_password_router = fastapi_users.get_reset_password_router()

verify_router = fastapi_users.get_verify_router(UserRead)


@verify_router.post("/exchange_verify_code")
async def exchange_verify_code(code: str):
    cache = get_cache_instance()
    token = cache.get(code)
    if token is None:
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT)
    cache.delete(code)
    return {"verify_token": token}


@auth_router.post("/auth/email/verify")
async def request_email_verification(user: User = Depends(current_user)):
    verify_email_token = uuid.uuid1().hex



@auth_router.post("/auth/email/verify/{code}/confirm")
async def confirm_email_verification(code: str,
                                     user: User = Depends(current_user),
                                     cache: StrictRedis = Depends(get_cache_instance),
                                     session: AsyncSession = Depends(get_async_session)):
    stored_token = cache.get(f"user_verify_{user.id}")
    if stored_token is None:
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT)
    if stored_token != code:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user.is_verified = True
    await session.commit()


class RestoreModel(BaseModel):
    email: str


@auth_router.post("/auth/restore")
async def restore(restore_obj: RestoreModel,
                  cache: StrictRedis = Depends(get_cache_instance),
                  session: AsyncSession = Depends(get_async_session)):
    statement = select(User).where(User.email == restore_obj.email)
    user = (await session.execute(statement)).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if not user.is_verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    restore_password_token = uuid.uuid1().hex

    msg = EmailMessage()
    msg.set_content(
        f"Hello {user.name}! Your restore password link: http://localhost:8000/auth/restore/{restore_password_token}/confirm"
    )
    msg['Subject'] = "MyLib restore password"
    msg['From'] = MAIL_SERVICE_EMAIL
    msg['To'] = user.email

    try:
        s = smtplib.SMTP()
        s.starttls()
        s.login(MAIL_SERVICE_EMAIL, MAIL_SERVICE_PASS)
        s.send_message(msg)
        s.quit()
    except Exception:
        raise HTTPException(status_code=503)  # Mail service unavailable

    await cache.set(restore_password_token, f"{user.id}", ex=MAIL_SERVICE_TOKEN_EXPIRATION_TIME)


# @auth_router.post("/auth/restore/{code}/confirm")
# async def confirm_reset_password(code: str,
#                                  response: Response,
#                                  cache: StrictRedis = Depends(get_cache_instance)):
#     if cache.get(code) is None:
#         raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT)
#     response.set_cookie(key='mylib_restore_code', value=code, httponly=True)
#
#
# class RestorePasswordModel(BaseModel):
#     password: str
#
#
# @auth_router.post("/auth/restore/submit")
# async def submit_reset_password(new_password_model: RestorePasswordModel,
#                                 response: Response,
#                                 mylib_restore_code: Cookie() = None,
#                                 cache: StrictRedis = Depends(get_cache_instance),
#                                 session: AsyncSession = Depends(get_async_session)):
#     user_id_str = await cache.get(f"user_restore_{mylib_restore_code}")
#     if user_id_str is None:
#         raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT)
#     user = await session.get(User, int(user_id_str))
#     user.rese
#     await cache.delete(mylib_restore_code)


current_user = fastapi_users.current_user()
