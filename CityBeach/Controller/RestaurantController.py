from Model.Product import *
from typing import List
from Model.Order import *
import re

pattern = re.compile(r'^[A-Za-z0-9 .]+$')

class AppRestaurantController:
    def __init__(self, products: List[Product], orders:List[Order]):
        self.products = products
        self.orders = orders
    def register_product(self,data) -> bool and int:
        try:
            name:str = data["name"]
            type:ProductType = data["type"]
            quantity = data["quantity"]
            price = data["price"]
            if not bool(pattern.match(name)) or name in [p.name for p in self.products]:
                return False, 1
            if quantity <= 0:
                return False, 2
            if price <= 0:
                return False, 3
            prod = Product(name=name,productType=type,quantity=quantity,price=price)
            self.products.append(prod)
            #print(f"PRODOTTO: {prod}")
            return True, 0
        except Exception as e:
            return False, -1

    def edit_product(self, product, qty_to_add)->bool:
        try:
            self.products[self.products.index(product)].quantity += qty_to_add
            return True
        except Exception as e:
            print(e)
            return False

    def remove_product(self,product_name:str):
        try:
            self.products.remove(self.get_product_by_name(product_name))
            return True
        except:
            return False

    def get_product_by_name(self,name:str)-> Product:
        return next((prod for prod in self.products if prod.name == name), None)
    
    def finalize_order(self, data):
        try:
            if not data:
                return False
            total_price = sum(prod.price * data[prod] for prod in data)

            for prod in data:
                prod.quantity -= data[prod]

            completed_order = Order(items=data, total_price=total_price)
            self.orders.append(completed_order)
            return True
        except Exception as e:
            print(f"Errore finalizzazione ordine: {e}")
            return False