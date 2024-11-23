import sqlite3
import json
import os
import time
from typing import List
from generateToken import Token
from timeit import default_timer as timer

class ApiDb ():
    def __init__(self):
        self.apiDb = "ApiDb.db"
        try:
            self.conn = sqlite3.connect(self.apiDb, check_same_thread=False)
            print("connection stablished")
        except:
            print("something went wrong")
        self.cursor = self.conn.cursor()
        self.dict = {}
        self.table = []
        self.token = Token()
        self.init = float

    def CreateDB(self):
        try:
            print(f"API DB is already created as {self.apiDb}")
        except:
            print(f"Something went wrong")

    def CreateTable(self):
        for item in self.table:
            self.cursor.execute(item)
        print("The table has been created correctly")

    def GetTable(self, int):
        if int == 0:
            self.cursor.execute("""SELECT * FROM Cars""")
            data = self.cursor.fetchall()
        elif int == 1:
            self.cursor.execute("""SELECT * FROM Users""")
            data = self.cursor.fetchall()    
        return data
    
    def GetItem(self, int, str):
        if int == 0:
            self.cursor.execute("""SELECT *
                                    FROM Cars
                                    WHERE id = {}""".format(str))
            data = self.cursor.fetchall()
            print(data)
        elif int == 1:
            self.cursor.execute("""SELECT *
                                    FROM Users
                                    WHERE id = {}""".format(str))
            data = self.cursor.fetchall()
            print(data)
        return data

    def AddToTable(self):
        try:
            self.cursor.execute(self.instruction, self.fields)
            print("Data have been added correctly")
            self.conn.commit()
        except Exception as e:
            print("There is an error {}".format(e))

    def SeeRow(self):
        data = self.cursor.execute('''SELECT * FROM Cars''')
        for row in data:
            print(row)

    def SetInstructionAndFieldsCar(self):
        self.StartCounting(timer())
        self.CompareTiming()
        self.instruction = '''INSERT INTO CARS(Brand, Model, Color, Year) VALUES(?,?,?,?)'''
        self.fields = (self.dict["brand"], self.dict["model"], self.dict["color"], int(self.dict["year"]))

    def SetInstructionAndFieldsUser(self):
        self.StartCounting(timer())
        self.CompareTiming()
        self.instruction = '''INSERT INTO USERS(Name, LastName, Email, Password, Position) VALUES(?,?,?,?,?)'''
        self.fields = (self.dict["name"], self.dict["lastName"], self.dict["email"], self.dict["password"], self.dict["position"])

    def SetInstructionAndFieldsChanges(self):
        self.StartCounting(timer())
        self.CompareTiming()
        self.instruction = '''INSERT INTO CHANGES(UserId, CarId) VALUES(?,?)'''
        self.fields = (self.dict["userId"], self.dict["carId"])

    def ProcessToCarTable(self):
        self.StartCounting(timer())
        self.CompareTiming()
        self.SetInstructionAndFieldsCar()
        self.AddToTable()

    def ProcessToUserTable(self):
        self.StartCounting(timer())
        self.CompareTiming()
        self.SetInstructionAndFieldsUser()
        self.AddToTable()

    def ProcessToRegister(self):
        self.StartCounting(timer())
        self.CompareTiming()
        self.SetInstructionAndFieldsChanges()
        self.AddToTable()

    def LogIn(self):
        data = self.GetUser()
        data = self.AutenticateUser(data)
        return data
    
    def GetUser(self):
        self.instruction = """SELECT id, Name, password FROM USERS WHERE Email = \"{}\" AND Password = \"{}\";""".format(self.dict["email"], self.dict["password"])
        self.cursor.execute(self.instruction)
        data = self.cursor.fetchall()
        return data
    
    def AutenticateUser(self, data):
        if len(data) != 0:
            self.token = self.token.GetToken()
            self.init = timer()
            self.StartCounting(timer())
            return "Autenticated"
        else:
            return "Credentials wrong or user do not exist"
        
    def StartCounting(self, end):
        try:
            self.timing = end - self.init
            print("This is the timing {} and token {}".format(self.timing, self.token))
        except Exception as e:
            print(e)
            
    def CompareTiming(self):
        if self.timing > 60.0:
            print(self.timing, self.timing>60.0)
            print("The token has expire please logIn again")
        else:
            print(self.timing, self.timing>60.0)
            print("The token remains useful")


if __name__ == "__main__":
    db = ApiDb()
    # Create CarTable
    db.table.append(""" CREATE TABLE IF NOT EXISTS CARS(
        id INTEGER PRIMARY KEY,
        Brand VARCHAR(255) NOT NULL,
        Model VARCHAR(255) NOT NULL,
        Color VARCHAR(255) NOT NULL,
        Year INTEGER NOT NULL,
        Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    ) """)
    # Create UserTable
    db.table.append("""CREATE TABLE IF NOT EXISTS USERS(
        id INTEGER PRIMARY KEY,
        Name VARCHAR(100) NOT NULL,
        LastName VARCHAR(100) NOT NULL,
        Email VARCHAR(100) NOT NULL,
        Password VARCHAR(100) NOT NULL,
        Position VARCHAR(100) NOT NULL,
        Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    # Create ChangesTable
    db.table.append(""" CREATE TABLE IF NOT EXISTS CHANGES(
        id INTEGER PRIMARY KEY,
        userId INTEGER,
        carId INTEGER,
        Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    ) """)
    db.CreateTable()
    # db.GetItem("2")