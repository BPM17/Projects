from pydantic import BaseModel, EmailStr

class User(BaseModel):
    username : str = None
    name : str = None
    lastName : str = None
    email : EmailStr = None
    password : str = None
    disabled : bool = None

class UserInDB(User):
    password: str