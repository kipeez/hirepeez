from abc import ABC, abstractmethod
from typing import List, Optional

from kipeez.data_logic.users import User


class UsersStorage(ABC):
    @classmethod
    async def reset(cls):
        """ reset storage"""
        pass
    @classmethod
    @abstractmethod
    async def get(cls, email: str = None, user_id: str = None) -> (User | None):
        pass
    @classmethod
    @abstractmethod
    async def update(cls, org_id: str, columns: List[str], values: List[str])-> bool:
        pass
    
    @classmethod
    @abstractmethod
    async def track_login(cls, user_id: str) -> List[User]:
        pass
    
    @classmethod
    @abstractmethod
    async def find(cls, ids: List[str]) -> List[User]:
        pass
    @classmethod
    @abstractmethod
    async def create(cls, email: str, hashed_password: str, first_name: Optional[str], last_name: Optional[str]) -> (bool):
        pass
    @classmethod
    @abstractmethod
    async def set_organisations(cls, user_id, organisations_ids) -> List[str]:
        pass
