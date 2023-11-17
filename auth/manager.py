import secrets
import smtplib
import string
import uuid
from email.message import EmailMessage
from typing import Optional

from fastapi import Depends, Request, HTTPException
from fastapi_users import BaseUserManager, IntegerIDMixin, schemas, models, exceptions
from redis import StrictRedis
from sqlalchemy.ext.asyncio import AsyncSession

from auth.database import get_user_db, get_async_session
from cache.cache import get_cache_instance
from config import BACKEND_USER_MANAGER_SECRET_KEY, MAIL_SERVICE_EMAIL, MAIL_SERVICE_PASS, \
    MAIL_SERVICE_TOKEN_EXPIRATION_TIME, MAIL_SERVICE_SMTP_SERVER
from models.models import User, Collection


class UserManager(IntegerIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = BACKEND_USER_MANAGER_SECRET_KEY
    verification_token_secret = BACKEND_USER_MANAGER_SECRET_KEY

    async def on_after_register(self, user: User, request: Optional[Request] = None,
                                session: AsyncSession = Depends(get_async_session)):
        print(f"User {user.id} has registered.")

        # Create Base collections
        base_collections = [
            Collection(
                title="Буду читать",
                user_id=user.id
            ),
            Collection(
                title="Читаю",
                user_id=user.id
            ),
            Collection(
                title="Прочитано",
                user_id=user.id
            ),
        ]

        session.add_all(base_collections)
        await session.commit()


    async def on_after_request_verify(self,
                                      user: User,
                                      token: str, request: Optional[Request] = None):
        print(f"User {user.id} requested verification")
        cache = get_cache_instance()
        alphabet = string.ascii_letters + string.digits
        while True:
            reset_code = ''.join([secrets.choice(alphabet) for _ in range(5)])
            if cache.get(reset_code) is None:
                cache.set(reset_code, token, ex=MAIL_SERVICE_TOKEN_EXPIRATION_TIME)
                break
        msg = EmailMessage()
        msg.set_content(
            f"Hello {user.name}! Your email verify code: {reset_code}"
        )
        msg['Subject'] = "MyLib email verification"
        msg['From'] = MAIL_SERVICE_EMAIL
        msg['To'] = user.email

        try:
            s = smtplib.SMTP(MAIL_SERVICE_SMTP_SERVER)
            s.starttls()
            s.login(MAIL_SERVICE_EMAIL, MAIL_SERVICE_PASS)
            s.send_message(msg)
            s.quit()
        except Exception:
            raise HTTPException(status_code=503)  # Mail service unavailable

    async def on_after_forgot_password(self, user: models.UP, token: str, request: Optional[Request] = None):
        print(f"User {user.id} requested verification")
        cache = get_cache_instance()
        while True:
            reset_code = secrets.token_hex(6)
            if cache.get(reset_code) is None:
                cache.set(reset_code, token, ex=MAIL_SERVICE_TOKEN_EXPIRATION_TIME)
                break
        msg = EmailMessage()
        msg.set_content(
            f"Hello {user.name}! Your reset password code: {reset_code}"
        )
        msg['Subject'] = "MyLib email verification"
        msg['From'] = MAIL_SERVICE_EMAIL
        msg['To'] = user.email

        try:
            s = smtplib.SMTP(MAIL_SERVICE_SMTP_SERVER)
            s.starttls()
            s.login(MAIL_SERVICE_EMAIL, MAIL_SERVICE_PASS)
            s.send_message(msg)
            s.quit()
        except Exception:
            raise HTTPException(status_code=503)  # Mail service unavailable

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:

        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["role_id"] = 1

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)