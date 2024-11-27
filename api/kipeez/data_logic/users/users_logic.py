from typing import List, Optional
from psycopg2 import Error
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from kipeez.data_storage.users.users_storage import UsersStorage
from kipeez.data_storage.organisations.organisations_storage import OrganisationsStorage
from kipeez.data_storage import StoragesProvider, DBStorage
from kipeez.data_logic.users import User, TokenData, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, RESET_TOKEN_EXPIRE_MINUTES
from kipeez.common.date.mocktime import mocktime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

class UsersLogic:
    users: UsersStorage
    organisations: OrganisationsStorage
    
    def __init__(self, storages: StoragesProvider | None = DBStorage()):
        self.users = storages.users()
        self.organisations = storages.organisations()

    async def create_user(self, email: str, password: str, first_name: Optional[str] = None, last_name: Optional[str] = None) -> str:
        hashed_password = get_password_hash(password)
        user_id = await self.users.create(email, hashed_password, first_name, last_name)
        return user_id
    async def update_password(self, user_id: str, password: str) -> bool:
        hashed_password = get_password_hash(password)
        await self.users.update(user_id, ['hashed_password'], [f"'{hashed_password}'"])
        return True
    async def update_hashed_password(self, user_id: str, hashed_password: str) -> bool:
        await self.users.update(user_id, ['hashed_password'], [f"'{hashed_password}'"])
        return True

    async def update(self, user_id: str, columns: List[str], values: List[str])-> bool:
        return await self.users.update(user_id, columns, values)
    
    async def authenticate_user(self, email: str, password: str = None, must_verify_password: bool = True) -> (User | None):
        user = await self.users.get(email=email)
        if not user:
            return None
        if must_verify_password and not verify_password(password, user.hashed_password):
            return None
        return user
    async def verify_password_for_user_id(self, user_id: str, password: str = None, must_verify_password: bool = True) -> (User | None):
        user = await self.users.get(user_id=user_id)
        if not user:
            return False
        return verify_password(password, user.hashed_password)
    async def get_user_from_id(self, user_id: str) -> (User | None):
        user = await self.users.get(user_id=user_id)
        if user is None:
            raise Exception(f"No user in db corresponding to the id "+user_id)
        return user
    
    async def get_user_from_email(self, email: str) -> (User | None):
        user = await self.users.get(email=email)
        if user is None:
            raise Exception(f"No user in db corresponding to the email "+email)
        return user
    
    async def get_user_from_token(self, token) -> (User | None):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str | None = payload.get("sub")
            if email is None:
                raise Exception("No email found in the jwt token")
            token_data = TokenData(email=email)
        except JWTError as e:
            raise e
        user = await self.users.get(email=token_data.email)
        if user is None:
            raise Exception("No user in db corresponding to the jwt token")
        return user
    
    async def track_user_login(self, user_id):
        return await self.users.track_login(user_id)
    
    async def find_users(self, users_ids:List[str] = []) -> List[User]:
        return await self.users.find(users_ids)

    def create_access_token(self, email:str, expires_delta: timedelta | None = None):
        data={"sub": email} 
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        expire = datetime.now(timezone.utc) + access_token_expires #dont mock or the jwt.decode will tell it expired
        to_encode = data.copy()
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def create_reset_token(self, email: str) -> str:
        expire =  datetime.now(timezone.utc) + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
        to_encode = {"sub": email, "exp": expire}
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    def verify_reset_token(self,token: str):
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise JWTError
        return email

    async def add_organisations(self, user_id: str, organisations_ids: List[str]):
        """ Add orgs to an user"""
        for organisation_id in organisations_ids:
            await self.organisations.add_user(organisation_id, user_id)
