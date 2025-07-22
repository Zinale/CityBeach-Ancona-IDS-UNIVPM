from dataclasses import field
from typing import Dict

import PyQt6

from Model.Booking import *
from Model.Data import TIME_SLOTS
from Model.Gender import Gender
from Model.Locker import Locker, LockerType


class AppBookingsController:
    def __init__(self, bookings: Dict[int, Booking], booking_id: int):
        self.bookings = bookings
        self.booking_id = booking_id

    def register_booking(self,data,currentUser:User,lockersList:List[Locker])->bool and int:
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

            #CREATE A NEW BOOKING
            lockerRoomUsageMale_list:List[LockerRoomUsage]=[]
            lockerRoomUsageFemale_list:List[LockerRoomUsage]=[]
            lockerRoomUsage_list:List[LockerRoomUsage]=[]
            if nMale>0:
                lockerRoomUsageMale_list = self.assign_locker_rooms(Gender.MALE, nMale, date_obj, timeSlot, lockersList)
                if not lockerRoomUsageMale_list:
                    return False, 13
                lockerRoomUsage_list.extend(lockerRoomUsageMale_list)
            if nFemale>0:
                lockerRoomUsageFemale_list = self.assign_locker_rooms(Gender.FEMALE, nFemale, date_obj, timeSlot, lockersList)
                if not lockerRoomUsageFemale_list:
                    return False, 13
                lockerRoomUsage_list.extend(lockerRoomUsageFemale_list)
            #for l in lockerRoomUsage_list:
            #    print(f"{l.gender.value} {l.players} {l.locker.name}")
            self.booking_id+=1
            dayTimeSlot = DayTimeSlot(day=date_obj,slot=(TIME_SLOTS[timeSlot:timeSlot+3]))
            self.bookings[self.booking_id] = Booking(field=field,nPlayers=nPlayer,nMale=nMale,nFemale=nFemale,
                                                     player=player,price=price,when=dayTimeSlot,lockers_usage=lockerRoomUsage_list,
                                                     id_booking=self.booking_id,usr_added_by=currentUser)
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
            if book.field.name == name and book.time.day == date and book.state in (BookingState.REGISTERED,BookingState.IN_PROGRESS) ]
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
            if b.field.name == name and b.time.day == date and b.state in (BookingState.REGISTERED,BookingState.IN_PROGRESS)
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

    def assign_locker_rooms(self,gender: Gender,n_players: int,date_obj: date,timeSlot: int,
            lockersList: List[Locker]) -> List[LockerRoomUsage]:

        assigned: List[LockerRoomUsage] = []

        preferred_lockers = [l for l in lockersList if gender.value==l.gender and l.type==LockerType.MAIN.value]
        support_lockers = [l for l in lockersList if l.type==LockerType.SECONDARY.value]
        individual_lockers = [l for l in lockersList if l.type == LockerType.INDIVIDUAL.value]
        active_bookings = [
            b for b in self.bookings.values()
            if b.time.day == date_obj and b.state in (BookingState.REGISTERED, BookingState.IN_PROGRESS)
        ]
        for b in active_bookings:
            for ts in b.time.slots:
                if ts.number in [s.number for s in TIME_SLOTS[timeSlot:timeSlot + 3]]:
                    for u in b.lockers_usage or []:
                        if u.gender not in (gender,Gender.OTHER.value):
                            pass
                            #support_lockers.remove(u.locker)
        print(f"spo prefe:{preferred_lockers}")
        print(f"spo suppo:{support_lockers}")
        print(f"spo indivi:{individual_lockers}")

        # Calcola occupazione corrente di un locker nella fascia richiesta
        def compute_locker_usage(lock: Locker) -> (int, set[Gender]):
            usage = 0
            genders = set()
            requested_slot_numbers = [s.number for s in TIME_SLOTS[timeSlot:timeSlot + 3]]
            for b in active_bookings:
                booked_slot_numbers = [s.number for s in b.time.slots]
                if any(slot in requested_slot_numbers for slot in booked_slot_numbers):
                    for u in b.lockers_usage or []:
                        if u.locker.name == lock.name:
                            usage += u.players
                            genders.add(u.gender)
            return usage, genders

        def allocate_from_list(locker_list: List[Locker]) -> int:
            nonlocal n_players
            for lock in locker_list:
                used, genders = compute_locker_usage(lock)
                print(f"Nome:{lock.name} Usati:{used} Generi:{genders}")
                if lock.gender == Gender.OTHER and genders and gender not in genders:
                    print("skidiosa")
                    continue  # già usato da altro genere
                if used >= lock.capacity:
                    print("asafa")
                    continue
                free = lock.capacity - used
                to_assign = min(free, n_players)
                assigned.append(LockerRoomUsage(lock, to_assign, gender))
                n_players -= to_assign
                if n_players <= 0:
                    break
            return n_players

        # Ordine di allocazione
        print(f"Da allocare {n_players} {gender.value}")
        remaining = allocate_from_list(preferred_lockers)
        print(f"Rimanenti: {remaining}")
        if remaining > 0:
            remaining = allocate_from_list(support_lockers)
        if remaining > 0:
            remaining = allocate_from_list(individual_lockers)

        if remaining > 0:
            return []  # spazio insufficiente

        return assigned
