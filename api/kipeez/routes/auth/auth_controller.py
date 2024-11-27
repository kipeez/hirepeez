from typing import List, Optional
from kipeez.data_logic.users.users_logic import UsersLogic
from kipeez.data_logic.organisations.organisations_logic import OrganisationsLogic
from kipeez.data_storage import StoragesProvider, DBStorage
from kipeez.data_logic.users import User, UserContextOrganisation, UserContext

class AuthControllerErrorInvalidToken(Exception):
    def __init__(self, token: str=None):
        super().__init__(f"{token} not valid")
        self.token = token
        
class AuthControllerErrorUserNotFound(Exception):
    def __init__(self, email: str=None):
        super().__init__(f"{email} not found")
        self.email = email
class AuthControllerImpersonateForbidden(Exception):
    def __init__(self, user_email: str=None):
        super().__init__(f"{user_email} cannot impersonate")
        self.user_email = user_email

class AuthController():
    
    users_logic: UsersLogic
    
    def __init__(self, storages: StoragesProvider | None = DBStorage()):
        self.users_logic =  UsersLogic(storages)
        self.organisations_logic =  OrganisationsLogic(storages)

    async def login(self, email, password) -> str | None:
        """ Login an user with password"""
        user = await self.users_logic.authenticate_user(email, password)
        if not user:
            return None
        await self.users_logic.track_user_login(user.id)
        return self.users_logic.create_access_token(user.email)

    async def get_user_context(self, token) -> UserContext:
        """ Get the logged user context querying the api"""
        user: User = await self.users_logic.get_user_from_token(token)
        organisations: List = await self.organisations_logic.get_organisations(user.organisations_ids)

        return UserContext(
            user_id=user.id,
            user_email=user.email,
            user_first_name=user.first_name,
            user_last_name=user.last_name,
            user_access_token=token,
            disabled=user.disabled,
            organisations=[UserContextOrganisation(
                name=o.name,
                id=o.id,
                slug=o.slug,
                permissions=["*"],
                role="owner" if o.owner_id == user.id else "user")
                for o in organisations
                ],
            )