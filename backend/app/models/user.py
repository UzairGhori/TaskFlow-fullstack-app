from datetime import datetime, timezone
from uuid import uuid4

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "app_user"
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    email: str = Field(unique=True, index=True)
    name: str = Field(max_length=255)
    password: str
    role: str = Field(default="user")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class UserCreate(SQLModel):
    name: str = Field(min_length=1, max_length=255)
    email: str = Field(min_length=3)
    password: str = Field(min_length=8)


class UserLogin(SQLModel):
    email: str
    password: str


class UserRead(SQLModel):
    id: str
    email: str
    name: str
    role: str
