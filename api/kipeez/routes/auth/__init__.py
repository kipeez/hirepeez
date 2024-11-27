from pydantic import BaseModel
from typing import List, Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class ResetPasswordParams(BaseModel):
    email: str
    update_password_link_prefix: Optional[str] = "https://app.kipeez.com/auth/reset-password"

class ImpersonateParams(BaseModel):
    email: str
class ResetPasswordConfirmParams(BaseModel):
    password: str
    token: str
  