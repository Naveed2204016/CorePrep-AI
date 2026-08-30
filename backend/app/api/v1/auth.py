from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from urllib.parse import urlencode
import os

from app.db.database import get_db
from app.models.user import User
from app.schemas.auth import SignupRequest, LoginRequest
from app.core.security import *
from fastapi import Request
from fastapi.responses import RedirectResponse
from app.core.google_auth import oauth


router = APIRouter(
    prefix="/api/v1/auth",
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
    db.refresh(new_user)


    return {
        "message":"Signup successful",
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email
        }
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
        "access_token":token,
        "user": {
            "id": db_user.id,
            "name": db_user.name,
            "email": db_user.email
        }
    }

@router.get("/google")
async def google_login(
    request:Request
):

    backend_url = os.getenv("BACKEND_PUBLIC_URL", "http://localhost:8000").rstrip("/")
    redirect_uri = f"{backend_url}/api/v1/auth/google/callback"

    return await oauth.google.authorize_redirect(
        request,
        redirect_uri
    )

@router.get("/google/callback")
async def google_callback(
    request:Request,
    db:Session=Depends(get_db)
):

    token = await oauth.google.authorize_access_token(
        request
    )

    user_info = token["userinfo"]


    email=user_info["email"]
    name=user_info["name"]
    google_id=user_info["sub"]


    user=db.query(User).filter(
        User.email==email
    ).first()


    if not user:

        user=User(
            name=name,
            email=email,
            google_id=google_id,
            auth_provider="google"
        )

        db.add(user)
        db.commit()
        db.refresh(user)


    jwt_token=create_token(
        {
            "user_id":user.id
        }
    )

    # Properly URL-encode the query parameters
    query_params = urlencode({
        "token": jwt_token,
        "id": user.id,
        "name": user.name,
        "email": user.email
    })

    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173").rstrip("/")
    return RedirectResponse(url=f"{frontend_url}/oauth-success?{query_params}")
