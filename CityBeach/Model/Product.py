import datetime
import uuid
from enum import Enum


class ProductType(Enum):
    DRINK = "Bevanda"
    ALCHOLIC_DRINK = "Alcool"
    SNACK = "Snack"
    FOOD= "Cibo"

class Product:
    def __init__(self, name:str,productType:ProductType,quantity:int, price:float):
        self.id = str(uuid.uuid4())
        self.name = name
        self.type = productType
        self.quantity = quantity
        self.price= price
        
    def isAvailable (self):  
        if self.quantity>0 : 
            return True
        return False
    def __str__(self):
        return f"{self.id} {self.name}"
    def __repr__(self):
        return f"{self.name}"
