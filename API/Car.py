from pydantic import BaseModel

class Car(BaseModel):
    brand : str = None
    model : str = None
    color : str = None
    year : int  = None