from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse


from kipeez.routes.auth.auth_controller import AuthController, AuthControllerErrorInvalidToken, AuthControllerErrorUserNotFound
from kipeez.routes.auth import ResetPasswordConfirmParams, ResetPasswordParams, Token, ImpersonateParams
from kipeez.routes.auth.routes import API_accounts_login_URL, API_accounts_password_URL
from kipeez.routes.auth.auth_controller import AuthController, AuthControllerImpersonateForbidden
from kipeez.routes.auth import Token
from fastapi.responses import JSONResponse
from kipeez.routes.auth.routes import API_accounts_login_URL, API_accounts_impersonate_URL
from kipeez.data_logic.users import UserContext
from kipeez.routes.auth.auth_methods import get_current_user_context
from kipeez.common.acl import UserPermission, has_permissions


router = APIRouter()
@router.post(API_accounts_login_URL)
async def API_accounts_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    controller = AuthController()
    access_token = await controller.login(form_data.username, form_data.password)
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(access_token=access_token, token_type="bearer")


@router.put(API_accounts_password_URL)
async def API_accounts_password_reset(params: ResetPasswordParams):
    controller = AuthController()
    await controller.send_reset_password(params.email, params.update_password_link_prefix)
    return JSONResponse(content={ "success": True } , status_code=202)

@router.post(API_accounts_password_URL) 
async def API_accounts_password_reset_confirm(params: ResetPasswordConfirmParams):
    controller = AuthController()
    try:
        success = await controller.confirm_reset_password(params.token, params.password)
        return JSONResponse(content={ "success": success } , status_code=200)
    except AuthControllerErrorInvalidToken:
        return JSONResponse(content={ "success": False, "detail":"Invalid token" }, status_code=403)
    except AuthControllerErrorUserNotFound:
        return JSONResponse(content={ "success": False, "detail":"Invalid token content" }, status_code=403)
    
