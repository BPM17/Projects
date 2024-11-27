from pydantic import BaseModel

class Token(BaseModel):
    accessToken : str
    tokenType : str

class TokenData(BaseModel):
    username : str | None = None