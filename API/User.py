from pydantic import BaseModel, EmailStr

class User(BaseModel):
    name : str = None
    lastName : str = None
    email : EmailStr = None
    password : str = None
    position : str = None