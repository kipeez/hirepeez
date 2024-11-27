import random
import string
import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from fastapi.testclient import TestClient

import pytest
import pytest_asyncio
from kipeez.main import app
from tests.tests_common.http_common import create_test_user, setupDB

from kipeez.routes.auth.routes import API_accounts_login_URL, API_accounts_impersonate_URL
from kipeez.routes.users.routes import API_users_me_URL
from kipeez.data_logic.users.users_logic import UsersLogic
client = TestClient(app)

@pytest_asyncio.fixture(scope="function", name="setup")
async def setup():
    await setupDB()

@pytest.mark.asyncio
async def test_create_and_login(setup):
    [error, user, _] = create_test_user(client)
    if error:
        print(error.json())
    assert not error
    assert user.id is not None

    logic = UsersLogic()

    users = await logic.find_users([user.id])
    assert len(users[0].last_logins) == 1

    response = client.post(
        API_accounts_login_URL,
        data={"username": user.email, "password": user.password },
        )
    assert response.status_code == 200, response.json()

    users = await logic.find_users([user.id])
    assert len(users[0].last_logins) == 2
