import os
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from kipeez.routes.auth.routes import API_accounts_login_URL
from dotenv import load_dotenv

if not os.getenv("JWT_SECRET"):
    load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET") # openssl rand -hex 32
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24*30
RESET_TOKEN_EXPIRE_MINUTES = 60*24
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl=API_accounts_login_URL)

class TokenData(BaseModel):
    email: str | None = None

class UserDashboard(BaseModel):
    id: str
    organisation_id: str
    is_owner: bool
    is_custom: bool
    key: str
    custom_title: str| None = None
    custom_description: str| None = None

class User(BaseModel):
    id: str
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    created_at: datetime | None = None
    disabled: bool | None = None
    hashed_password: str | None = None
    organisations_ids: List[str] = []
    last_logins: List[datetime] = []

class UserContextOrganisation(BaseModel):
    id: str
    slug: str
    name: str
    role: str
    permissions: List[str]


class UserContext(BaseModel):
    disabled: bool
    user_id: str
    user_email: str | None = None
    user_first_name: str | None = None
    user_last_name: str | None = None
    user_access_token: str | None = None
    organisations: List[UserContextOrganisation] | None = None

