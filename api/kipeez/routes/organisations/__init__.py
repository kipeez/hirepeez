from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional



class OrganisationDefinition(BaseModel):
    name: str
    slug: Optional[str] = None

class OrganisationDefinitionAndExtras(BaseModel):
    id: str
    owner_id: Optional[str] = None
    owner_email: Optional[str] = None
    owner_first_name: Optional[str] = None
    owner_last_name: Optional[str] = None
    config: OrganisationDefinition

class OrganisationUser(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    is_owner: bool
    created_at: datetime
    last_logins: List[datetime]
