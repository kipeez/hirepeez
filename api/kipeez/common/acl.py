from enum import Enum
from typing import List

class UserPermission(Enum):
    BACKOFFICE = "BACKOFFICE"

async def has_permissions(user_email: str, permission: List[UserPermission]) -> bool:
    if user_email in [
        'admins@kipeez.com',
        'js@kipeez.com',
        'cguenel@kipeez.com',
        'bdechenaud@kipeez.com',
        'mkasrani@kipeez.com',
        'rbourbilieres@kipeez.com',
        'oguillemot@kipeez.com',
        'gohanrga@gmail.com']:
        return True
    return False