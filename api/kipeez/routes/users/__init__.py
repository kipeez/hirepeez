from pydantic import BaseModel
from typing import List, Optional

class UsersAddOrganisationsParams(BaseModel):
    user_id: List[str]
    organisations_ids: List[str]

class CreateAccountParams(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    organisation_name: Optional[str] = None

class UserMenuOrganisation(BaseModel):
    name: str
    slug: str
    id: str

class UserMenuTodo(BaseModel):
    organisation_id: str
    count: int

class UserMenu(BaseModel):
     organisations: List[UserMenuOrganisation]
     todos: List[UserMenuTodo]

class UserAttributes(BaseModel):
    first_name:Optional[str]=None
    last_name:Optional[str]=None
    email:Optional[str]=None
    current_password:Optional[str]=None
    new_password:Optional[str]=None