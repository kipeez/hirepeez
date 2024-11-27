import asyncio
import sys
import os



sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from kipeez.data_storage import DBStorage
from kipeez.data_logic.organisations.organisations_logic import OrganisationsLogic
from kipeez.data_logic.users.users_logic import UsersLogic
from kipeez.data_logic.users import User

async def main():

    users_logic = UsersLogic()
    organisations_logic = OrganisationsLogic()

    print("Reset the DB")
    await DBStorage().reset()
    print("insert defaults data")

    hire:User = await users_logic.get_user_from_email("hire@kipeez.com")

    await organisations_logic.create_organisation("aidviz", hire.id, "aidviz")

    print("Set up DONE")
if __name__ ==  '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())