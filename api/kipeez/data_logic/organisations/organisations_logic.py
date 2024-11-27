from typing import List, Optional

from slugify import slugify
from kipeez.data_logic.organisations import Organisation,  OrganisationConfigAnalysis
from kipeez.data_storage import StoragesProvider, DBStorage
from kipeez.data_storage.organisations.organisations_storage import OrganisationsStorage
from kipeez.data_storage.users.users_storage import UsersStorage
from kipeez.data_logic.users import User

class OrganisationsLogic:
    organisations: OrganisationsStorage
    
    def __init__(self, storages: StoragesProvider | None = DBStorage()):
        self.organisations = storages.organisations()
        self.users = storages.users()

    async def create_organisation(self, name: str, owner_id: str, slug: str | None = None) -> (str):
        """ Create an org and returns its id """
        if not slug:
            slug = slugify(name)
        organisations_id = await self.organisations.create(name, slug, owner_id)
        return organisations_id
    

    async def find_organisations(self, organisations_ids:List[str] = []) -> List[Organisation]:
        return await self.organisations.find(organisations_ids)
    
    async def get_organisation_from_slug(self, organisation_slug) -> Optional[Organisation]:
        return await self.organisations.get(slug=organisation_slug)
    
    async def add_user(self, organisation_id, user_id) -> bool:
        """ add an user to an organisation """
        org:Organisation | None = await self.get(organisation_id)
        if org is None:
            print("Cannot add user to an unknow org "+ organisation_id)
            return False
        return await self.organisations.add_user(organisation_id, user_id)
 

    async def set_owner(self, organisation_id, user_id) -> bool:
        """ set an user as an organisation owner """
        org:Organisation | None = await self.get(organisation_id)
        if org is None:
            print("Cannot set owner of an unknow org "+ organisation_id)
            return False
        
        await self.organisations.add_user(organisation_id, user_id)
        return await self.organisations.update(organisation_id, ["owner_id"], [f"UUID('{user_id}')"])

    async def get(self, organisation_id: str) -> Organisation | None:
        orgs:List[Organisation] = await self.organisations.find([organisation_id])
        if not orgs:
            return None
        return orgs[0]
    
    async def update(self, organisation_id,
                     name: str = None,
                     slug: str = None,
                     ) -> bool:
        """ update an organisation fields """
        fields=[]
        values=[]
        if name:
            fields.append("name")
            values.append(f"'{name}'")
        if slug:
            fields.append("slug")
            values.append(f"'{slug}'")
        if not fields:
            return False
        return await self.organisations.update(organisation_id, fields, values)


    async def get_organisations(self, organisations_ids: List[str]) -> List[Organisation]:
        if not organisations_ids:
            return []
        return await self.organisations.find(organisations_ids)