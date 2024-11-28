# General Imports
import json
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

# My Imports
from apiDb import ApiDb
from Car import Car
from User import User, UserInDB
from Token import Token, TokenData


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#Objects and Variables
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()

items = []
users = []
cars = []
db = ApiDb()

def VerifyPassword(plainPassword, password):
    return pwd_context.verify(plainPassword, password)

def GetPasswordHash(password):
    return pwd_context.hash(password)

def GetUserTokenExample(userList, username : str):
    if username in userList:
        userList = userList[username]
        return UserInDB(**userList)
    
def AuthenticateUser(db, username : str, password : str):
    user = GetUserTokenExample(db, username)
    if not user:
        return False
    if not VerifyPassword(password, user.password):
        return False
    return user

def CreateAccessToken(data: dict, expiresDelta : timedelta | None = None):
    toEncode = data.copy()
    if expiresDelta:
        expire = datetime.now(timezone.utc) + expiresDelta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    toEncode.update({"exp":expire})
    encodedJwt = jwt.encode(toEncode, SECRET_KEY, algorithm=ALGORITHM)
    return encodedJwt

userList = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "name": "Alice",
        "lastName": "Wonderson",
        "email": "alice@example.com",
        "password": "fakehashedsecret2",
        "disabled": True,
    },
}

# Functions
@app.get("/")
def root():
    return{"Title: This API is intended to consume vehicle data, from a DB created in from SQLite3"}

@app.get("/users/me/{User}")
async def ReadUserMe(user : User):
    db.dict = dict(user)
    data = db.LogIn()
    return data

# User Section init
# CRUD operations
@app.put("/User/{User}")
async def PutUser(user : User):
    users.append({"User" : user})
    db.dict = dict(user)
    db.ProcessToUserTable()
    return "The User has been added correctly"

@app.get("/Users")
async def GetUsers():
    data = db.GetTable(1)
    return data

@app.get("/Users/{username}")
async def GetUser(username:str):
    data = db.GetItem(1,username)
    return data

# Car section init
# CRUD operations

@app.put("/Car/{Car}")
async def PostCar(car : Car):
    cars.append({"Car" : car})
    db.dict = dict(car)
    db.ProcessToCarTable()
    return "The Car has been added correctly"

def FakeHashPassword(password:str):
    return "fakehashed" + password

def GetUserDict(db, username : str):
    if username in db:
        userDict = db[username]
        return UserInDB(**userDict)

def GetCurrentUser(token: Annotated[str, Depends(oauth2_scheme)]):
    credentialsException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers= {"WWW-Authenticate":"Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username : str = payload.get("sub")
        if username is None:
            raise credentialsException
        tokenData = TokenData(username=username)
    except InvalidTokenError:
        raise credentialsException
    user = GetUserTokenExample(userList, username=tokenData.username)
    if user is None:
        raise credentialsException
    return user

async def GetCurrentActiveUser(
        currentUser : Annotated[User, Depends(GetCurrentUser)],
):
    if currentUser.disabled:
        raise HTTPException(status_code = 400, detail = "Inactive User")
    return currentUser

@app.post("/token")
async def LoginForAccessToken(formData: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    print("Executing Login for access token")
    userDict = AuthenticateUser(userList, formData.username, formData.password)
    print(formData.password,formData.username, formData.client_id, formData.client_secret)
    if not userDict:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate" : "Bearer"},
        )
    accessTokenExpires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    accessToken = CreateAccessToken(
        data = {"sub" : userDict.username}, expiresDelta=accessTokenExpires
    )
    print(accessToken)
    return Token(accessToken=accessToken, tokenType="bearer")

@app.get("/user/me")
async def ReadUser(
    currentUser: Annotated[User, Depends(GetCurrentActiveUser)]
    ):
    print(currentUser)
    return currentUser

@app.get("/user/me/items")
async def ReadOwnItems(
    currentUser: Annotated[User, Depends(GetCurrentActiveUser)],
):
    return[{"itemId": "Foo", "owner": currentUser.username}]

@app.get("/Car/")
async def GetCars1(token: Annotated[str, Depends(oauth2_scheme)]):
    # The difference between this function and the other is also the dependency of oauth2_scheme
    # This function it is just the frontend for the endpoint
    return {"token": token}

@app.get("/Car")
async def GetCars():
    data = db.GetTable(0)
    return data

@app.get("/Car/{carId}")
def GetCar(carId:str):
    data = db.GetItem(0, carId)
    return data