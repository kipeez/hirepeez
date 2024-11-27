from typing import Annotated

from fastapi import Depends, APIRouter

from kipeez.routes.users.routes import API_users_me_URL, API_users_menu_URL, API_users_URL
from kipeez.routes.auth.auth_methods import get_current_user_context
from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException
from fastapi.responses import JSONResponse

from kipeez.routes.users.users_controller import UsersController
from kipeez.data_logic.users import UserContext
from kipeez.routes.auth import Token
from kipeez.routes.users import CreateAccountParams, UserAttributes
from kipeez.routes.users import UsersAddOrganisationsParams

router = APIRouter()



@router.post(API_users_URL)
async def API_users_create(
    form_data: CreateAccountParams) -> Token:
    email = form_data.email
    password = form_data.password
    first_name = form_data.first_name
    last_name = form_data.last_name
    organisation_name = form_data.organisation_name
    controller = UsersController()
    user_id = await controller.create_user(email, password, first_name, last_name, organisation_name)
    if not user_id:
        raise HTTPException(
            status_code=500,
            detail="Impossible to create the user",
        )
    return JSONResponse({ "success": True, "data": { "id": user_id }  })

@router.get(API_users_me_URL)
async def API_users_me(user_context: Annotated[UserContext, Depends(get_current_user_context)]):
 
    return JSONResponse({ 
        "success": True,
        "data": {
            "id": user_context.user_id,
            "email": user_context.user_email,
            "first_name": user_context.user_first_name,
            "last_name": user_context.user_last_name,
            "organisations": [o.model_dump() for o in user_context.organisations],
            "access_token": user_context.user_access_token
        }
    })
@router.put(API_users_me_URL)
async def API_users_me(attributes:UserAttributes, user_context: Annotated[UserContext, Depends(get_current_user_context)]):
    if not attributes.first_name and not attributes.first_name and not attributes.last_name and not attributes.email and not attributes.current_password:
        return JSONResponse({ 
            "success": False
        })
    controller = UsersController()
    success = await controller.update_user_attributes(user_context.user_id,
                first_name=attributes.first_name,
                last_name=attributes.last_name,
                email=attributes.email,
                current_password=attributes.current_password,
                new_password=attributes.new_password)
    return JSONResponse({ 
        "success": success
    })