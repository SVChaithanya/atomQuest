from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from passlib.context import CryptContext
from jose import JWTError, jwt

from datetime import datetime, timedelta, timezone

import uuid
import hashlib
import os

from db import get_db
from models import USERS, RefreshToken


# =========================================
# CONFIG
# =========================================

SECRET_KEY = os.getenv("SECURITY","surya_super_secret_key")

ALGORITHM = "HS256"

ACCESS_TOKEN_MINUTES = 15

REFRESH_TOKEN_DAYS = 7


# =========================================
# PASSWORD HASHING
# =========================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str):

    return pwd_context.hash(password[:72])


def verify_password(
    plain_password: str,
    hashed_password: str
):

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# =========================================
# ACCESS TOKEN
# =========================================

def create_access_token(user_id: str):

    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc)
        + timedelta(minutes=ACCESS_TOKEN_MINUTES)
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# =========================================
# REFRESH TOKEN
# =========================================

def hash_refresh_token(token: str):

    return hashlib.sha256(
        token.encode()
    ).hexdigest()


def create_refresh_token(
    user_id: str,
    db: Session
):

    raw_token = str(uuid.uuid4())

    hashed_token = hash_refresh_token(raw_token)

    db_token = RefreshToken(
        user_id=user_id,
        token_hash=hashed_token,
        expire=datetime.now(timezone.utc)
        + timedelta(days=REFRESH_TOKEN_DAYS)
    )

    db.add(db_token)

    db.commit()

    return raw_token


# =========================================
# OAUTH
# =========================================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


# =========================================
# CURRENT USER
# =========================================

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials"
    )

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = (
        db.query(USERS)
        .filter(USERS.id == user_id)
        .first()
    )

    if not user:
        raise credentials_exception

    return user