import random
import string
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient

from kipeez.main import app
from tests.tests_common.http_common import setupDB, create_test_user_and_login

from kipeez.routes.users.routes import API_users_me_URL


client = TestClient(app)

@pytest_asyncio.fixture(scope="function", name="setup")
async def setup():
    """ setup the DB"""
    await setupDB()

@pytest.mark.asyncio
async def test_user_me(setup):
    [error, user, _] = create_test_user_and_login(client)
    assert not error, error.json()
    # get context
    response = client.get(API_users_me_URL, headers=user.headers)
    assert response.status_code == 200, response.json()
    context = response.json()["data"]
    assert len(context) == 6, "context does not return enough or returns too much fields"
    assert context["id"]
    assert context["email"]
    assert context["first_name"]
    assert context["last_name"]
    assert context["organisations"]
    assert context["organisations"][0]["id"]
    assert context["organisations"][0]["name"]
    assert context["access_token"]


