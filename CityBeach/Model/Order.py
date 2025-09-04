import datetime
import uuid
from typing import List
from typing import Dict
from Model.Product import *

class Order:
    def __init__(self, items:Dict[Product, int], total_price:float):
        self.id = str(uuid.uuid4())
        self.items = items
        self.total_price = total_price
        self.timestamp = datetime.datetime.now()

    def __repr__(self):
        return f"Order(id={self.id}, total_price={self.total_price:.2f})"