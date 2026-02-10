from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.dependencies.auth import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.dependencies.database import get_session
from app.models.user import User, UserCreate, UserLogin, UserRead

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(body: UserCreate, session: Session = Depends(get_session)):
    # Check if email already exists
    existing = session.exec(
        select(User).where(User.email == body.email)
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    user = User(
        name=body.name,
        email=body.email,
        password=hash_password(body.password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.post("/token")
def login(body: UserLogin, session: Session = Depends(get_session)):
    # Find user by email
    user = session.exec(
        select(User).where(User.email == body.email)
    ).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Verify password
    if not verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Create JWT token
    access_token = create_access_token(data={
        "sub": user.id,
        "email": user.email,
        "name": user.name,
        "role": user.role,
    })

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
        },
    }
