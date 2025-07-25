from dataclasses import field
from typing import Dict

import PyQt6
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QMessageBox
from datetime import datetime
from Model.Booking import *
from Model.Data import TIME_SLOTS
from Model.Gender import Gender
from Model.Locker import Locker, LockerType


class AppBookingsController:
    def __init__(self, bookings: Dict[int, Booking], booking_id: int):
        self.bookings = bookings
        self.booking_id = booking_id
        self.timerLastTrigger = None

    def check_and_update(self):
        now = datetime.now()
        hour =now.hour
        minute = now.minute
        if True or (minute == 0 or minute == 30) and (self.timerLastTrigger != (hour, minute)):
            self.timerLastTrigger = (hour, minute)
            for b in list(self.bookings.values()):
                if b.state == BookingState.REGISTERED:
                    if b.time.day == now.date():
                        if hour > b.time.slots[0].startTime.hour or (hour == b.time.slots[0].startTime.hour and minute >= b.time.slots[0].startTime.minute):
                            b.state = BookingState.IN_PROGRESS
                if b.state == BookingState.IN_PROGRESS:
                    if b.time.day == now.date():
                        if hour > b.time.slots[2].endTime.hour or (hour == b.time.slots[2].endTime.hour and minute >= b.time.slots[2].endTime.minute):
                            b.state = BookingState.COMPLETED

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
                lockerRoomUsageMale_list = self.assign_locker_rooms(gender=Gender.MALE, n_players=nMale, date_obj=date_obj, timeSlot=timeSlot, lockersList=lockersList)
                if not lockerRoomUsageMale_list:
                    return False, 13
                lockerRoomUsage_list.extend(lockerRoomUsageMale_list)
            self.booking_id+=1
            dayTimeSlot = DayTimeSlot(day=date_obj,slot=(TIME_SLOTS[timeSlot:timeSlot+3]))
            self.bookings[self.booking_id] = Booking(field=field,nPlayers=nPlayer,nMale=nMale,nFemale=nFemale,
                                                     player=player,price=price,when=dayTimeSlot,lockers_usage=lockerRoomUsage_list,
                                                     id_booking=self.booking_id,usr_added_by=currentUser)

            if nFemale>0:
                lockerRoomUsageFemale_list = self.assign_locker_rooms(gender=Gender.FEMALE, n_players=nFemale, date_obj=date_obj, timeSlot=timeSlot, lockersList=lockersList)
                if not lockerRoomUsageFemale_list:
                    return False, 13
                self.bookings[self.booking_id].lockers_usage.extend(lockerRoomUsageFemale_list)
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


    def assign_locker_rooms(self, gender: Gender, n_players: int, date_obj: date, timeSlot: int,
                            lockersList: List[Locker]) -> List[LockerRoomUsage]:

        assigned: List[LockerRoomUsage] = []

        # Dividi locker per tipo
        preferred_lockers = [l for l in lockersList if gender == l.gender and l.type == LockerType.MAIN.value]
        support_lockers = [l for l in lockersList if l.type == LockerType.SECONDARY.value]
        individual_lockers = [l for l in lockersList if l.type == LockerType.INDIVIDUAL.value]

        print(len(preferred_lockers))
        # Fascia oraria richiesta
        requested_slots = TIME_SLOTS[timeSlot:timeSlot + 3]
        requested_start = requested_slots[0].startTime
        requested_end = requested_slots[-1].endTime

        # Prenotazioni attive nella data richiesta (inserita)
        active_bookings = [
            b for b in list(self.bookings.values())
            if b.time.day == date_obj and b.state in (BookingState.REGISTERED, BookingState.IN_PROGRESS)
        ]

        # Spogliatoi secondari o individuali già occupati da altro genere nella stessa fascia
        occupied_support_lockers = set()
        for b in active_bookings:
            booking_slots = b.time.slots
            if not booking_slots:
                continue

            booking_start = booking_slots[0].startTime
            booking_end = booking_slots[-1].endTime

            if not (requested_end <= booking_start or requested_start >= booking_end):
                for u in b.lockers_usage or []:
                    if u.gender != gender and u.locker.type in (LockerType.SECONDARY, LockerType.INDIVIDUAL):
                        occupied_support_lockers.add(u.locker.name)

        # Spogliatoi già occupati da altro genere
        support_lockers = [l for l in support_lockers if l.name not in occupied_support_lockers]
        individual_lockers = [l for l in individual_lockers if l.name not in occupied_support_lockers]

        print(f"spo prefe: {preferred_lockers}")
        print(f"spo suppo: {support_lockers}")
        print(f"spo indivi: {individual_lockers}")

        def compute_locker_usage(lock: Locker) -> tuple[int, set[Gender]]:
            usage = 0
            genders = set()
            for b in active_bookings:
                booking_slots = b.time.slots
                if not booking_slots:
                    continue

                booking_start = booking_slots[0].startTime
                booking_end = booking_slots[-1].endTime
                print(f"CHECK: {booking_start} {booking_end}")
                if not (requested_end <= booking_start or requested_start >= booking_end):
                    print("for")
                    for u in b.lockers_usage or []:
                        print(f"CHECK: Spogliatoio: {lock.name}")
                        if u.locker.name == lock.name:
                            usage += u.players
                            genders.add(u.gender)
                            break  # conta solo una volta per booking-locker (altrimenti conta x3 fasce)
            return usage, genders

        def allocate_from_list(locker_list: List[Locker]) -> int:
            nonlocal n_players
            for lock in locker_list:
                used, genders = compute_locker_usage(lock)
                print(f"Nome: {lock.name} Usati: {used} Generi: {genders}")
                print(f"CHECK: Genere:{type(gender)}:{gender}, {genders}")
                if lock.type in (LockerType.SECONDARY.value,
                                 LockerType.INDIVIDUAL.value) and genders and gender not in genders:
                    print("Spogliatoio occupato da genere diverso, salto")
                    continue

                if used >= lock.capacity:
                    continue

                free = lock.capacity - used
                to_assign = min(free, n_players)
                assigned.append(LockerRoomUsage(lock, to_assign, gender))
                n_players -= to_assign
                if n_players <= 0:
                    break
            return n_players

        print(f"Da allocare: {n_players} {gender}")
        remaining = allocate_from_list(preferred_lockers)
        print(f"Rimanenti dopo MAIN: {remaining}")
        if remaining > 0:
            remaining = allocate_from_list(support_lockers)
        if remaining > 0:
            remaining = allocate_from_list(individual_lockers)

        if remaining > 0:
            print("ERRORE: Spazio insufficiente")
            return []

        for assi in assigned:
            print(f"Assegnato: {assi.locker.name} {assi.players} {assi.gender}")
        print("\n\n")
        return assigned

    def print_locker_status_by_slot(self, date_obj: date, lockers_list: List[Locker]):
        from collections import defaultdict
        from Model.Data import TIME_SLOTS
        from Model.Locker import LockerType
        from Model.Gender import Gender

        # Dict: slot_label -> locker_name ->  gender -> count
        slot_map = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

        locker_gender_map = {locker.name: locker.gender for locker in lockers_list}
        locker_type_map = {locker.name: locker.type for locker in lockers_list}

        # Prenotazioni attive per quella data
        active_bookings = [
            b for b in self.bookings.values()
            if b.time.day == date_obj and b.state in (BookingState.REGISTERED, BookingState.IN_PROGRESS)
        ]

        for booking in active_bookings:
            for ts in booking.time.slots:
                slot_label = f"{ts.startTime.strftime('%H:%M')}-{ts.endTime.strftime('%H:%M')}"
                for usage in booking.lockers_usage or []:
                    gender = usage.gender.name.capitalize()
                    slot_map[slot_label][usage.locker.name][gender] += usage.players

        # slot (str)
        all_slot_labels = [f"{ts.startTime.strftime('%H:%M')}-{ts.endTime.strftime('%H:%M')}" for ts in TIME_SLOTS]
        all_locker_names = sorted({locker.name for locker in lockers_list})

        print(f"\nStato spogliatoi per il {date_obj.strftime('%d/%m/%Y')} (analisi ogni 30 minuti)\n")

        for slot_label in all_slot_labels:
            print(f"Fascia: {slot_label}")
            lockers_in_slot = slot_map.get(slot_label, {})

            for locker_name in all_locker_names:
                locker_gender = locker_gender_map.get(locker_name, Gender.OTHER)
                locker_type = locker_type_map.get(locker_name, LockerType.SECONDARY)

                gender_counts = lockers_in_slot.get(locker_name, {})

                print(f"  Spogliatoio {locker_name}:")

                if not gender_counts:
                    print("     - Vuoto")
                    continue

                if locker_type in (LockerType.SECONDARY.value, LockerType.INDIVIDUAL.value) and len(gender_counts) > 1:
                    print("     ERRORE: contiene più generi!")
                    for gender, count in gender_counts.items():
                        print(f"     - {gender}: {count} giocatori")
                else:
                    for gender, count in gender_counts.items():
                        print(f"     - {gender}: {count} giocatori")
            print()