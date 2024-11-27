from typing import List, Optional

from slugify import slugify
from kipeez.data_logic.organisations.organisations_logic import OrganisationsLogic
from kipeez.data_storage import StoragesProvider, DBStorage
from kipeez.routes.organisations import OrganisationDefinition, OrganisationDefinitionAndExtras
from kipeez.data_logic.users.users_logic import UsersLogic

class OrganisationsControllerErrorOrganisationNotFound(Exception):
    def __init__(self, organisation_id: str=None):
        super().__init__(f"{organisation_id} not found")
        self.organisation_id = organisation_id

class OrganisationsControllerErrorUserNotFound(Exception):
    def __init__(self, user_id: str=None):
        super().__init__(f"{user_id} not found")
        self.user_id = user_id

class OrganisationsControllerErrorNotOwner(Exception):
    def __init__(self, user_id: str=None, organisation_id: str=None):
        super().__init__(f"{user_id} not owner of {organisation_id}")
        self.user_id = user_id
        self.organisation_id = organisation_id

class OrganisationsControllerErrorNotInTheOrganisation(Exception):
    def __init__(self, user_id: str = None, organisation_id: str=None):
        super().__init__(f"user{user_id} not in the organisation {organisation_id}")
        self.user_id = user_id
        self.organisation_id = organisation_id

class OrganisationsControllerErrorInvitationNotFound(Exception):
    def __init__(self, invitation_id: str=None):
        super().__init__(f"{invitation_id} not found")
        self.invitation_id = invitation_id

class OrganisationsControllerErrorInvitationNotGuest(Exception):
    def __init__(self, invitation_id: str=None, user_email: str=None):
        super().__init__(f"{invitation_id} not for f{user_email}")
        self.invitation_id = invitation_id
        self.user_email = user_email

class OrganisationsControllerErrorDuplicateSlug(Exception):
    def __init__(self, slug: str=None):
        super().__init__(f"an organisation with the same slug {slug}, already exists")
        self.slug = slug

class OrganisationsController():
    
    organisations_logic: OrganisationsLogic
    users_logic: UsersLogic
    
    def __init__(self, storages: StoragesProvider | None = DBStorage()):
        self.organisations_logic =  OrganisationsLogic(storages)
        self.users_logic =  UsersLogic(storages)

    async def add_organisation(self, name: str, owner_id: str, slug: Optional[str] = None) -> List[str]:
        """ Create an organisation"""
        organisation_slug = slug if slug else slugify(name)
        if await self.organisations_logic.get_organisation_from_slug(organisation_slug):
            raise OrganisationsControllerErrorDuplicateSlug(organisation_slug)

        organisation_id = await self.organisations_logic.create_organisation(name, owner_id, organisation_slug)
        return [organisation_id, organisation_slug]
    
    
    async def update_organisation_owner(self, organisation_id: str, current_owner_id: str, next_owner_email: str) -> bool:
        organisation = await self.organisations_logic.get(organisation_id)
        if not organisation:
            raise OrganisationsControllerErrorOrganisationNotFound()
        if current_owner_id not in organisation.users_ids:
            raise OrganisationsControllerErrorNotInTheOrganisation()
        if organisation.owner_id != current_owner_id:
            raise OrganisationsControllerErrorNotOwner()
        next_owner = await self.users_logic.get_user_from_email(next_owner_email)
        if not next_owner:
            raise OrganisationsControllerErrorUserNotFound()
        if organisation.owner_id != current_owner_id:
            raise OrganisationsControllerErrorNotOwner()
        return await self.organisations_logic.set_owner(organisation_id, next_owner.id)
           
    async def get_organisation_config(self, organisation_id: str, requester_id: str) -> OrganisationDefinitionAndExtras:
        organisation = await self.organisations_logic.get(organisation_id)
        if not organisation:
            raise OrganisationsControllerErrorOrganisationNotFound()
        if requester_id not in organisation.users_ids:
            raise OrganisationsControllerErrorNotInTheOrganisation()
        owner = await self.users_logic.get_user_from_id(organisation.owner_id)
        return OrganisationDefinitionAndExtras(
            id=organisation.id,
            owner_id=owner.id,
            owner_first_name=owner.first_name,
            owner_last_name=owner.last_name,
            owner_email=owner.email,
            config=OrganisationDefinition(name=organisation.name, slug=organisation.slug) 
        )
    

    async def set_organisation_config(self, organisation_id: str, definition: OrganisationDefinition, requester_id: str) -> bool:
        organisation = await self.organisations_logic.get(organisation_id)
        if not organisation:
            raise OrganisationsControllerErrorOrganisationNotFound()
        if requester_id not in organisation.users_ids:
            raise OrganisationsControllerErrorNotInTheOrganisation()
        if organisation.owner_id != requester_id:
            raise OrganisationsControllerErrorNotOwner()
        return await self.organisations_logic.update(organisation_id,
                                                     name=definition.name,
                                                     slug=definition.slug,
                                                     ) 