from typing import Optional
from slugify import slugify
from kipeez.data_logic.users.users_logic import UsersLogic
from kipeez.data_logic.organisations.organisations_logic import OrganisationsLogic
from kipeez.data_storage import StoragesProvider, DBStorage


class UsersController():
    
    users_logic: UsersLogic
    organisations_logic: OrganisationsLogic
    
    def __init__(self, storages: StoragesProvider | None = DBStorage()):
        self.users_logic =  UsersLogic(storages)
        self.organisations_logic =  OrganisationsLogic(storages)
    
    async def create_user(self, email: str, password: str, first_name: Optional[str], last_name: Optional[str], organisation_name: Optional[str]) -> (str):
        """ Create a user with password"""
        if not email:
            return None
        user_id = await self.users_logic.create_user(email, password, first_name, last_name)
        if user_id and organisation_name:
            slug = slugify(organisation_name)
            await self.organisations_logic.create_organisation(organisation_name, user_id, slug)
        return user_id
    
    
    async def update_user_attributes(self, user_id: str,
                       first_name:Optional[str]=None,
                       last_name:Optional[str]=None,
                       email:Optional[str]=None,
                       current_password:Optional[str]=None,
                       new_password:Optional[str]=None,
                    ) -> bool:
        """ update an user attributes """
        if email or new_password:
            if not current_password:
                print("Forbidden to update email without password")
                return False
            if not await self.users_logic.verify_password_for_user_id(user_id, current_password):
                print("Forbidden to update user with a wrong password")
                return False
        columns = []
        values = []
        if first_name:
            columns.append("first_name")
            values.append(f"'{first_name}'")
        if last_name:
            columns.append("last_name")
            values.append(f"'{last_name}'")
        if email:
            columns.append("email")
            values.append(f"'{email}'")
        res = True if not columns else await self.users_logic.update(user_id, columns, values)
        if not res:
            return False
        if new_password:
            return await self.users_logic.update_password(user_id, new_password)
        return True