import unittest

from Model.Product import *
from Model.Data import AppData
from Controller.RestaurantController import AppRestaurantController


class RestaurantTestCase(unittest.TestCase):
    def setUp(self):
        self.model = AppData()
        self.model.save_to_file = lambda path: None
        self.restaurant_controller = AppRestaurantController(self.model.products,self.model.orders)
        self.data_product ={
            "name": "Acqua Naturale 0.5l",
            "type": ProductType("Bevanda"),
            "quantity":20,
            "price": 1
        }

    def test_register_editQty_remove_product(self):
        success_registration = self.restaurant_controller.register_product(self.data_product)
        self.assertTrue(success_registration)
        prod = self.restaurant_controller.get_product_by_name("Acqua Naturale 0.5l")

        edit_qty_result = self.restaurant_controller.edit_product(product=prod,qty_to_add=10)
        self.assertTrue(edit_qty_result)
        self.assertEqual(prod.quantity,30)      #20+10

        removed = self.restaurant_controller.remove_product("Acqua Naturale 0.5l")
        self.assertTrue(removed)

    def test_create_order(self):
        self.restaurant_controller.register_product(self.data_product)
        data_order = {}
        data_order[self.restaurant_controller.get_product_by_name("Acqua Naturale 0.5l")] = 5
        success = self.restaurant_controller.finalize_order(data_order)
        self.assertTrue(success)
        self.assertEqual(self.restaurant_controller.orders[0].total_price,
                         5 * self.data_product["price"])
        self.assertEqual(self.restaurant_controller.get_product_by_name(
            "Acqua Naturale 0.5l").quantity,15)


if __name__ == "__main__":
    unittest.main()
