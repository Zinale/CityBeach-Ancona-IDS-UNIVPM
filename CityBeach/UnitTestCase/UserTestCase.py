import unittest
from datetime import date

from PyQt6.QtCore import QDate

from Model.Data import AppData
from Controller.UsersController import AppUsersController
from Model.Gender import Gender


class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.model = AppData()
        self.model.save_to_file = lambda path: None
        self.user_controller = AppUsersController(self.model.users, self.model.users_next_id)
        self.data =  {"name": "admin","surname": "admin",
            "username": "admin","birthday": QDate(1, 1, 1).toString("dd/MM/yyyy"),
            "is_admin": True,"gender": Gender.OTHER}
        self.data_MarioRossi  = {"name": "Mario","surname": "Rossi","username": "mRossi",
            "birthday": date(2025,1,1).strftime("%d/%m/%Y"),
            "is_admin": True,"gender": Gender.OTHER}

    def test_register_login_logout(self):
        success_registration = self.user_controller.register(self.data, password="password")
        self.assertTrue(success_registration)

        success_login  = self.user_controller.login(username="admin", password="password")
        self.assertTrue(success_login)
        self.assertIsNotNone(self.user_controller.get_current_user())

        not_login = self.user_controller.login(username="admin", password="admin")
        self.assertFalse(not_login)

        self.user_controller.logout()
        self.assertIsNone(self.user_controller.get_current_user())

    def test_edit_user(self):
        success = self.user_controller.register(self.data, password="password")
        self.assertTrue(success)
        login = self.user_controller.login(username="admin", password="password")
        self.assertTrue(login)

        success = self.user_controller.register(data=self.data_MarioRossi,password="")
        self.assertTrue(success)
        success=(self.user_controller.edit_user(user_id=self.user_controller.user_id,new_name="Mario",
            new_gender=Gender.MALE,new_surname="Rossi",
            new_birthday=date(2025,1,1).strftime("%d/%m/%Y"),
            new_password="mRoss25",new_username="MRoss1"))
        self.assertTrue(success)
        self.user_controller.logout()
        new_login = self.user_controller.login("MRoss1","mRoss25")
        self.assertTrue(new_login)

    def test_delete_user(self):
        self.user_controller.register(self.data, password="password")
        self.user_controller.login(username="admin", password="password")
        self.user_controller.register(data=self.data_MarioRossi,password="")

        success = self.user_controller.delete_user(
            self.user_controller.get_user_by_username("mRossi"))
        self.assertTrue(success)

        not_success, state = self.user_controller.delete_user(self.user_controller.get_current_user())
        self.assertFalse(not_success)
        self.assertEqual(state,1)



if __name__ == "__main__":
    unittest.main()
