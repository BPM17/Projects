import uuid
import random
import os

class Token():
    def __init__(self):
        self.token = ""
    
    def GetToken(self):
        return uuid.uuid4()

if __name__ == "__main__":
    token = Token()
    token = token.GetToken()
    print(token)