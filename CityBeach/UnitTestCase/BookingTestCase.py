import unittest

from PyQt6.QtCore import QDate
from datetime import date, timedelta

from Model.Data import AppData
from Model.Locker import *
from Model.Field import *
from Model.Booking import *
from Controller.UsersController import AppUsersController
from Controller.BookingsController import AppBookingsController
from Controller.FieldsController import AppFieldsController
from Controller.LockersController import AppLockersController
from Controller.PlayersController import AppPlayersController

class BookingTestCase(unittest.TestCase):
    def setUp(self):
        self.model = AppData()
        self.model.save_to_file = lambda path: None
        #register and login
        self.user_controller = AppUsersController(
            self.model.users, self.model.users_next_id)
        self.data =  {"name": "admin","surname": "admin",
            "username": "admin",
            "birthday":QDate(1, 1, 1).toString("dd/MM/yyyy"),
            "is_admin": True,"gender": Gender.OTHER}
        self.user_controller.register(self.data, password="password")
        self.user_controller.login(username="admin", password="password")

        self.booking_controller = AppBookingsController(
            self.model.bookings,self.model.bookings_next_id)
        self.field_controller = AppFieldsController(
            self.model.fields,self.model.fields_next_id)
        self.locker_controller = AppLockersController(
            self.model.lockers,self.model.lockers_next_id)
        self.player_controller = AppPlayersController(
            self.model.players,self.model.players_next_id)
        self.data_field = {"name": "Padel-1","sport": FieldType("Padel")}
        self.data_locker = {"name": "Maschi-1","gender": Gender("M"),
            "capacity": 15,"type": LockerType("Principale")}
        self.data_player = {"name": "Mario","surname":"Rossi",
            "birthday": date(2025,1,1).strftime("%d/%m/%Y"),
            "gender": Gender("M"),"phone":"+393333333333",
            "email":"mail@email.org","city":"Ancona"}


    def test_register_field(self):
        success_registration = self.field_controller.register_field(
            self.data_field,self.user_controller.get_current_user())
        self.assertTrue(success_registration)

    def test_register_locker(self):
        success_registration = self.locker_controller.register_locker(
            self.data_locker,self.user_controller.get_current_user())
        self.assertTrue(success_registration)

    def test_register_player(self):
        success_registration = self.player_controller.register_player(
            self.data_player, self.user_controller.get_current_user())
        self.assertTrue(success_registration)

    def test_register_booking(self):
        self.test_register_field()
        self.test_register_locker()
        self.test_register_player()
        field = self.field_controller.get_field_by_name(self.data_field["name"])
        player = self.player_controller.findByEmail(self.data_player["email"])
        data_booking = {"sport":Sports("Padel"),"field": field,
                "player": player,"nPlayer":4,"nMale":4,
                "nFemale":0,"price":50,
                "date": (date.today()+timedelta(days=1)).strftime("%d/%m/%Y"),
                "timeSlot": 0}
        success, state = self.booking_controller.register_booking(data_booking,
                self.user_controller.current_user,
                list(self.locker_controller.lockers.values()))
        self.assertTrue(success)
        self.assertEqual(state,0)       #Prenotazione effettuata

        data_not_booking = data_booking.copy()
        success, state = self.booking_controller.register_booking(data_not_booking,
                self.user_controller.current_user,
                list(self.locker_controller.lockers.values()))
        self.assertFalse(success)
        self.assertEqual(state,12)              #Campo Occupato


if __name__ == "__main__":
    unittest.main()