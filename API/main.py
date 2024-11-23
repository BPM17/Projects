# General Imports
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from passlib.context import CryptContext

# My Imports
from apiDb import ApiDb
from Car import Car
from User import User

#Objects and Variables
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "token")

items = []
users = []
cars = []
db = ApiDb()

# Functions
@app.get("/")
def root():
    return{"Title: This API is intended to consume vehicle data, from a DB created in from SQLite3"}

def FakeDecodeToken(token):
    return User(
        userName = token + "fakecode", email = "johndoe@example.com", full_name = "John Doe"
    )

def GetCurrentUser(token : Annotated[str, Depends(oauth2_scheme)]):
    user = FakeDecodeToken(token)
    return user

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

@app.get("/Users/{userId}")
async def GetUser(userId:str):
    data = db.GetItem(1,userId)
    return data

# Car section init
# CRUD operations
@app.put("/Car/{Car}")
async def PostCar(car : Car):
    cars.append({"Car" : car})
    db.dict = dict(car)
    db.ProcessToCarTable()
    return "The Car has been added correctly"

@app.get("/Car")
async def GetCars():
    data = db.GetTable(0)
    return data

@app.get("/Car/{carId}")
def GetCar(carId:str):
    data = db.GetItem(0, carId)
    return data