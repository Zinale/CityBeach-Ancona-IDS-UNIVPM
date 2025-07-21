from typing import Dict
from Model.Booking import *

class AppBookingsController:
    def __init__(self, bookings: Dict[int, Booking], booking_id: int):
        self.bookings = bookings
        self.booking_id = booking_id

    def register_booking(self,data,currentUser:User)->bool and int:
        print(data)
        return