from abc import ABC, abstractmethod
from kipeez.data_storage.users.users_storage import UsersStorage
from kipeez.data_storage.organisations.organisations_storage import OrganisationsStorage

class StoragesProvider(ABC):
    @abstractmethod
    def users(self) -> UsersStorage:
        pass
    @abstractmethod
    def organisations(self) -> OrganisationsStorage:
        pass

    