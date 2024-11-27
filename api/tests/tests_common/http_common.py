import random
import string
from typing import Union
from fastapi import Response
from pydantic import BaseModel
from fastapi.testclient import TestClient

from kipeez.routes.auth.routes import API_accounts_login_URL
from kipeez.routes.users.routes import API_users_URL, API_users_me_URL
from kipeez.routes.organisations.routes import API_organisations_URL
from kipeez.routes.users.routes import API_users_me_URL
from kipeez.data_storage import DBStorage

class UserAndHeaders(BaseModel):
    email: str
    headers: dict

class TestUser(BaseModel):
    email: str
    id: str
    password: str

class TestOrganisation(BaseModel):
    name: str
    id: str

async def setupDB():
    await DBStorage().reset()
    

def create_test_organisation(client: TestClient, email: str, password: str) -> Union[Response, TestOrganisation]:

    response = client.post(
        API_accounts_login_URL,
        data={"username": email, "password": password },
        )
    if response.status_code != 200:
        return [response, None]
    json_response = response.json()
    headers = {"Authorization": f"Bearer {json_response['access_token']}"}


    name = 'unittest-'+''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))
    response = client.post(
        API_organisations_URL,
        json={"name": name },
        headers=headers
        )
    if response.status_code != 200:
        return [response, None]
    assert name is not None
    id = response.json()["data"]["id"]
    assert id is not None
    return [None, TestOrganisation(name = name, id = id)]

def create_test_user(client: TestClient, email = None) -> Union[Response, TestUser, TestOrganisation]:
    email = email if email else 'unittest@'+''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))+".com"
    password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
    organisation_name = 'unittest-'+''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))
    response = client.post(
        API_users_URL,
        json={"email": email, "password": password, "first_name": email, "last_name": password, "organisation_name": organisation_name },
        )

    if response.status_code != 200:
        return [response, None, None]

    user_id = response.json()["data"]["id"]
    assert user_id is not None

    response = client.post(
        API_accounts_login_URL,
        data={"username": email, "password": password },
        )
    if response.status_code != 200:
        return [response, None]
    json_response = response.json()
    headers = {"Authorization": f"Bearer {json_response['access_token']}"}
    response = client.get(
        url=API_users_me_URL,
        headers=headers,
        )
    
    json_response = response.json()
    return [None,
            TestUser(email=email, id=user_id, password=password),
            TestOrganisation(name=organisation_name, id=json_response["data"]["organisations"][0]["id"])
            ]



def create_test_user_and_login(client: TestClient) -> Union[Response,UserAndHeaders, TestOrganisation]:
    [response, user, organisation] = create_test_user(client)
    if response:
        return [response, None]
    
    response = client.post(
        API_accounts_login_URL,
        data={"username": user.email, "password": user.password },
        )
    if response.status_code != 200:
        return [response, None]
    json_response = response.json()
    return [None, UserAndHeaders(email=user.email, headers = {"Authorization": f"Bearer {json_response['access_token']}"}), organisation]
