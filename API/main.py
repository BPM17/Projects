# General Imports
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from passlib.context import CryptContext
import json
import jwt

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

------------------------------------------------------------------------------------------

items = []
users = []
cars = []
db = ApiDb()

userList = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
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

@app.get("/token")
async def ReadToken(token: Annotated[str, Depends(oauth2_scheme)]):
    return{"token":token}

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

def FakeDecodeToken(token):
    user = GetUserDict(userList, token)
    return user
    # return User(
    #     username = token + "fakedecoded", email = "john@example.com", name = "John Doe"
    # )

def GetCurrentUser(token: Annotated[str, Depends(oauth2_scheme)]):
    user = FakeDecodeToken(token)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid authentication credentials",
            headers = {"WWW-Authenticate" : "Bearer"},
        )
    return user

async def GetCurrentActiveUser(
        currentUser : Annotated[User, Depends(GetCurrentUser)],
):
    if currentUser.disabled:
        raise HTTPException(status_code = 400, detail = "Inactive User")
    return currentUser

@app.post("/token")
async def login(formData: Annotated[OAuth2PasswordRequestForm, Depends()]):
    userDict = userList.get(formData.username)
    if not userDict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**userDict)
    password = FakeHashPassword(formData.password)
    if not password == user.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    return {"access_token": user.username, "token_type": "bearer"}

async def GetUserMe(token: Annotated[str, Depends(oauth2_scheme)]):
    user = FakeDecodeToken(token)
    return user

@app.get("/user/me")
async def ReadUser(
    current_user: Annotated[User, Depends(GetCurrentActiveUser)]
    ):
    return current_user

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