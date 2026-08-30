import os

from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User


SECRET_KEY = os.getenv("SECRET_KEY", "coreprep-dev-only-change-me")
ALGORITHM = "HS256"

security = HTTPBearer()

pwd_context = CryptContext(
    schemes=["bcrypt"]
)


def hash_password(password):
    return pwd_context.hash(password)


def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)


def create_token(data):
    return jwt.encode(
        data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    token = credentials.credentials


    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("user_id")


        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="No user_id in token"
            )


        user = db.query(User).filter(
            User.id == int(user_id)
        ).first()


        if user is None:
            raise HTTPException(
                status_code=401,
                detail="User not found"
            )


        return {
            "id": user.id,
            "email": user.email,
            "name": user.name
        }


    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
