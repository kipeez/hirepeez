from datetime import timezone
from typing import Annotated, List

from fastapi import Depends, APIRouter, HTTPException

from fastapi.responses import RedirectResponse

from kipeez.routes.organisations.organisations_controller import OrganisationsController, OrganisationsControllerErrorDuplicateSlug, OrganisationsControllerErrorInvitationNotFound, OrganisationsControllerErrorInvitationNotGuest, OrganisationsControllerErrorOrganisationNotFound, OrganisationsControllerErrorNotInTheOrganisation, OrganisationsControllerErrorNotOwner, OrganisationsControllerErrorUserNotFound
from kipeez.routes.organisations.routes import API_organisations_URL
from kipeez.routes.organisations.routes import API_organisations_invitation_create_URL
from kipeez.routes.organisations.routes import API_organisations_invitation_accept_URL
from kipeez.routes.organisations.routes import API_organisations_users_URL
from kipeez.routes.organisations.routes import API_organisations_owner_URL
from kipeez.routes.organisations.routes import API_organisations_config_URL

from kipeez.common.date.serialize import serialize_date, serialize_dates
from kipeez.routes.organisations import OrganisationUser, OrganisationDefinition


from fastapi.responses import JSONResponse

from kipeez.data_logic.users import UserContext
from kipeez.routes.auth.auth_methods import get_current_user_context, get_current_user_context_no_fail

router = APIRouter()

@router.post(API_organisations_URL)
async def API_organisations_create(body: OrganisationDefinition,  user_context: Annotated[UserContext, Depends(get_current_user_context)]):
    controller = OrganisationsController()
    try:
        [organisation_id, organisation_slug] = await controller.add_organisation(body.name, user_context.user_id, body.slug)
        if not organisation_id:
            return JSONResponse(content={ "success": False, "detail":"Impossible to create the organisation" }, status_code=500)
        return JSONResponse({ "success": True, "data": { "id": organisation_id, "slug": organisation_slug} })
    except OrganisationsControllerErrorDuplicateSlug:
        return JSONResponse(content={ "success": False, "detail":"Duplicate Slug", "error_code": "DC" }, status_code=200)


@router.put(API_organisations_owner_URL)
async def API_organisations_owner(organisation_id: str,  user_email: str, user_context: Annotated[UserContext, Depends(get_current_user_context)]):
    try:
        controller = OrganisationsController()
        if await controller.update_organisation_owner(organisation_id, user_context.user_id, user_email):
            return JSONResponse({ "success": True, "data": {"organisation_id": organisation_id, }})
        else:
            return JSONResponse({ "success": False, "detail": "Impossible to update" })
    except OrganisationsControllerErrorOrganisationNotFound:
       return JSONResponse(content = { "success": False, "detail":"Unknown organisations" }, status_code=404)
    except OrganisationsControllerErrorUserNotFound:
       return JSONResponse(content={ "success": False, "detail":"Unknown user" }, status_code=404 )
    except OrganisationsControllerErrorNotInTheOrganisation:
       return JSONResponse(content={ "success": False, "detail":"Forbidden" }, status_code=403)
    except OrganisationsControllerErrorNotOwner:
       return JSONResponse(content={ "success": False, "detail":"Forbidden" }, status_code=403)
    except Exception as e:
       print(e)
       return JSONResponse(content={ "success": False, "detail":"Unknown Error" }, status_code=404)

@router.get(API_organisations_config_URL)
async def API_organisations_config_get(organisation_id: str, user_context: Annotated[UserContext, Depends(get_current_user_context)]):
    try:
        controller = OrganisationsController()
        config = await controller.get_organisation_config(organisation_id, user_context.user_id)
        return JSONResponse({ "success": True, "data": config.model_dump() })
    except OrganisationsControllerErrorOrganisationNotFound:
        return JSONResponse(content = { "success": False, "detail":"Unknown organisations" }, status_code=404)
    except OrganisationsControllerErrorNotInTheOrganisation:
        return JSONResponse(content={ "success": False, "detail":"Forbidden" }, status_code=403)
    except Exception as e:
        print(e)
        return JSONResponse(content={ "success": False, "detail":"Unknown Error" }, status_code=404)

@router.put(API_organisations_config_URL)
async def API_organisations_config_put(organisation_id: str, config: OrganisationDefinition, user_context: Annotated[UserContext, Depends(get_current_user_context)]):
    try:
        controller = OrganisationsController()
        success = await controller.set_organisation_config(organisation_id, config, user_context.user_id)
        return JSONResponse({ "success": success })
    except OrganisationsControllerErrorOrganisationNotFound:
        return JSONResponse(content = { "success": False, "detail":"Unknown organisations" }, status_code=404)
    except OrganisationsControllerErrorNotInTheOrganisation:
        return JSONResponse(content={ "success": False, "detail":"Forbidden" }, status_code=403)
    except OrganisationsControllerErrorNotOwner:
        return JSONResponse(content={ "success": False, "detail":"Forbidden" }, status_code=403)
    except Exception as e:
        print(e)
        return JSONResponse(content={ "success": False, "detail":"Unknown Error" }, status_code=404)


