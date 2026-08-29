from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.auth import SignupRequest, LoginRequest
from app.core.security import *


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/signup")
def signup(
    user:SignupRequest,
    db:Session=Depends(get_db)
):

    existing = db.query(User).filter(
        User.email == user.email
    ).first()


    if existing:
        raise HTTPException(
            400,
            "Email already exists"
        )


    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(
            user.password
        )
    )


    db.add(new_user)
    db.commit()


    return {
        "message":"Signup successful"
    }



@router.post("/login")
def login(
    user:LoginRequest,
    db:Session=Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == user.email
    ).first()


    if not db_user:
        raise HTTPException(
            401,
            "Invalid credentials"
        )


    if not verify_password(
        user.password,
        db_user.password
    ):
        raise HTTPException(
            401,
            "Invalid credentials"
        )


    token=create_token(
        {
            "user_id":db_user.id
        }
    )


    return {
        "access_token":token
    }