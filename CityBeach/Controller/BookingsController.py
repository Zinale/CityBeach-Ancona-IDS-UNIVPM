from dataclasses import field
from typing import Dict

import PyQt6

from Model.Booking import *
from Model.Data import TIME_SLOTS


class AppBookingsController:
    def __init__(self, bookings: Dict[int, Booking], booking_id: int):
        self.bookings = bookings
        self.booking_id = booking_id

    def register_booking(self,data,currentUser:User)->bool and int:
        try:
            #validate data
            if data["sport"] is None:
                return False, 1
            sport = data["sport"]
            if data["field"] is None:
                return False, 2
            field = data["field"]
            if data["player"] is None:
                return False, 3
            player= data["player"]
            if data["nPlayer"] is None or data["nPlayer"] <=0:
                return False,4
            nPlayer = data["nPlayer"]
            if data["nMale"] is None:
                return False, 5
            nMale = data["nMale"]
            if data["nFemale"] is None:
                return False, 6
            nFemale = data["nFemale"]
            if data["price"] is None:
                return False, 7
            price = data["price"]
            if data["date"] is None:
                return False, 8
            date = data["date"]
            date_obj = datetime.strptime(date, "%d/%m/%Y").date()
            if data["timeSlot"] is None:
                return False, 9
            timeSlot = data["timeSlot"]
            if nPlayer != nMale+nFemale:
                return False,10
            data_splitted = date.split("/")
            if PyQt6.QtCore.QDate(int(data_splitted[2]), int(data_splitted[1]), int(data_splitted[0])) < PyQt6.QtCore.QDate.currentDate():
                return False, 11
            if not self.checkAvailabilityField(field.name, date_obj, timeSlot):
                return False, 12

            self.booking_id+=1
            dayTimeSlot = DayTimeSlot(day=date_obj,slot=(TIME_SLOTS[timeSlot:timeSlot+3]))
            self.bookings[self.booking_id] = Booking(field=field,nPlayers=nPlayer,nMale=nMale,nFemale=nFemale,
                                                     player=player,price=price,when=dayTimeSlot,
                                                     id_booking=self.booking_id,usr_added_by=currentUser)
            print(self.bookings[self.booking_id])
            return True, 0

        except Exception as e:
            print(f"Errore: {type(e)}")
            print(f"Messaggio: {e}")
            return False, -1


    def checkAvailabilityField(self, name: str, date: date, timeSlot: int):
        requested_slots = TIME_SLOTS[timeSlot:timeSlot + 3]
        requested_start = requested_slots[0].startTime
        requested_end = requested_slots[2].endTime
        matched_bookings = [book for book in self.bookings.values()
            if book.field.name == name and book.time.day == date]
        for booking in matched_bookings:
            for booked_slot in booking.time.slots:
                booked_start = booked_slot.startTime
                booked_end = booked_slot.endTime
                if not (requested_end <= booked_start or requested_start >= booked_end):
                    return False
        return True
    def getAvailableTimeSlots(self, name: str, date: date) -> List[int]:
        available_slots = []
        bookings_on_date = [
            b for b in self.bookings.values()
            if b.field.name == name and b.time.day == date
        ]
        booked_slot_numbers = set()
        for booking in bookings_on_date:
            for slot in booking.time.slots:
                booked_slot_numbers.add(slot.number)

        for i in range(len(TIME_SLOTS) - 2):  #25
            blocco = [i + 1, i + 2, i + 3]  # gli slot.number partono da 1
            if all(s not in booked_slot_numbers for s in blocco):
                available_slots.append(i)

        return available_slots
