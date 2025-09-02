from Model.Product import Product
from typing import List
class ProductsController:
    def __init__(self, products: List[Product]):
        self.products = products
        
