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
        self.id = str(uuid.uuid3())
        self.name = name
        self.type = productType
        self.quantity = quantity
        self.price= price
        
    def isAvailable (self):  
        if self.quantity>0 : 
            return True
        return False