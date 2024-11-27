import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from kipeez.main import app
from tests.tests_common.http_common import create_test_organisation, create_test_user, setupDB


client = TestClient(app)

@pytest_asyncio.fixture(scope="function", name="setup")
async def setup():
    """ setup the DB"""
    await setupDB()

@pytest.mark.asyncio
async def test_create_organisation(setup):
    [error, user, _] = create_test_user(client)
    [error, organisation] = create_test_organisation(client, user.email, user.password)
    if error:
        print(error.json())
    assert not error
    assert organisation.name is not None
    assert organisation.id is not None