from typing import Annotated
from fastapi import Depends, HTTPException, status
from kipeez.routes.auth.auth_controller import AuthController
from kipeez.data_logic.users import UserContext, OAUTH2_SCHEME

async def get_current_user_context(token: Annotated[str, Depends(OAUTH2_SCHEME)]) -> UserContext:
    try:
        controller = AuthController()
        user = await controller.get_user_context(token)
        if not user:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
            )

        if user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return user
    except Exception as e:
        print(e)
        raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Error getting context",
        headers={"WWW-Authenticate": "Bearer"},
    )

async def get_current_user_context_no_fail(token: Annotated[str, Depends(OAUTH2_SCHEME)]) -> UserContext:
    try:
        return await get_current_user_context(token)
    except Exception as e:
        return None
