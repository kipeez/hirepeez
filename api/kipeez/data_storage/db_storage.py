from kipeez.data_storage import StoragesProvider
from kipeez.data_storage.users.users_storage import UsersStorage
from kipeez.data_storage.users.users_db import UsersDB
from kipeez.data_storage.organisations.organisations_storage import OrganisationsStorage
from kipeez.data_storage.organisations.organisations_db import OrganisationsDB


class DBStorage(StoragesProvider):
    """ Storage from database"""
    async def reset(self):
        await UsersDB.reset()
        await OrganisationsDB.reset()
    
    def users(self) -> UsersStorage:
        return UsersDB

    def organisations(self) -> OrganisationsStorage:
        return OrganisationsDB
