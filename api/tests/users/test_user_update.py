import sys
import os



sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import pytest_asyncio
import pytest
import os
from kipeez.data_storage import DBStorage
from kipeez.data_logic.organisations.organisations_logic import OrganisationsLogic
from kipeez.data_logic.users.users_logic import UsersLogic
from kipeez.data_logic.users import User

from kipeez.routes.users.users_controller import UsersController

org_name = "acme"

user_email = "user"
user_pwd = "user"


@pytest_asyncio.fixture(scope="function", name="user_id")
async def fixture_user_id():
    """ create the owner user (that will create the org)"""
    await DBStorage().reset()
    users_logic = UsersLogic()
    user_id = await users_logic.create_user(user_email, user_pwd)
    assert user_id
    return user_id

@pytest_asyncio.fixture(scope="function", name="org_id")
async def fixture_org_id(user_id):
    """ create the org with the admin user as owner"""
    organisations_logic = OrganisationsLogic()
    org_id = await organisations_logic.create_organisation(org_name, user_id)
    assert org_id
    return org_id


@pytest.mark.asyncio
async def test_update(org_id, user_id):
    users_controller = UsersController()
    users_logic = UsersLogic()

    # first_name
    assert await users_controller.update_user_attributes(user_id, first_name="newf")
    user: User = await users_logic.get_user_from_id(user_id)
    assert user.first_name == "newf"
    # last_name
    assert await users_controller.update_user_attributes(user_id, last_name="newl")
    user: User = await users_logic.get_user_from_id(user_id)
    assert user.last_name == "newl"

    #email
    assert not await users_controller.update_user_attributes(user_id, email="newe")
    assert not await users_controller.update_user_attributes(user_id, email="newe", current_password="toto")
    assert await users_controller.update_user_attributes(user_id, email="newe", current_password=user_pwd)
    user: User = await users_logic.get_user_from_id(user_id)
    assert user.email == "newe"

    #password
    assert not await users_controller.update_user_attributes(user_id, new_password="newep")
    assert not await users_controller.update_user_attributes(user_id, new_password="newep", current_password="toto")
    assert await users_controller.update_user_attributes(user_id, new_password="newep", current_password=user_pwd)
    assert not await users_logic.authenticate_user(user_email, user_pwd)
    assert not await users_logic.authenticate_user(user_email, "newep")




# Running pytest directly
if __name__ == "__main__":
    pytest.main([__file__])
