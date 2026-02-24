from pydantic import BaseModel
from typing import Optional



class UserSchema(BaseModel):
    name: str
    lastname: Optional[str] = None
    email : str
    password: str
    username: str
    birthday: Optional[str] = None
    city: Optional[str] = None




class TokenSchema(BaseModel):
    access_token: str
    token_type: str
