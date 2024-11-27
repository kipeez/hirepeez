from abc import ABC, abstractmethod
from typing import List

from kipeez.data_logic.organisations import Organisation


class OrganisationsStorage(ABC):
    @classmethod
    async def reset(cls):
        """ reset storage"""
        pass
    @classmethod
    @abstractmethod
    async def create(cls, name: str, slug: str, owner_id: str):
        pass
    @classmethod
    @abstractmethod
    async def update(cls, org_id: str, columns: List[str], values: List[str])-> bool:
        pass
    @classmethod
    @abstractmethod
    async def find(cls, ids: List[str]) -> List[Organisation]:
        pass
    @classmethod
    @abstractmethod
    async def get(cls, id: str = None, slug: str = None) -> (Organisation | None):
        pass
    @classmethod
    @abstractmethod
    async def add_user(cls, organisation_id, user_id) -> bool:
        pass