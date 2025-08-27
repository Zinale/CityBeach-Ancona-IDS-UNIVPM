from typing import Dict
import PyQt6
import matplotlib.pyplot as plt
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QPixmap, QImage


from Model.Booking import *
from Model.Data import TIME_SLOTS
from Model.Gender import Gender
from Model.Locker import Locker, LockerType
from io import BytesIO


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
                                                     id_booking=self.booking_id,usr_added_by=currentUser, sport=sport)

            if nFemale>0:
                lockerRoomUsageFemale_list = self.assign_locker_rooms(gender=Gender.FEMALE, n_players=nFemale, date_obj=date_obj, timeSlot=timeSlot, lockersList=lockersList)
                if not lockerRoomUsageFemale_list:
                    del self.bookings[self.booking_id]
                    return False, 13
                self.bookings[self.booking_id].lockers_usage.extend(lockerRoomUsageFemale_list)
            return True, 0
        except Exception as e:
            print(f"Messaggio: {e}")
            return False, -1

    def checkAvailabilityFieldAtTimeSLot(self,field:Field,date:date,slot:int):
        matched_bookings = [b for b in self.bookings.values() if b.field.name == field.name and b.time.day == date and b.state in (BookingState.REGISTERED,BookingState.IN_PROGRESS,BookingState.COMPLETED)]
        for b in matched_bookings:
            if slot in [i.number for i in b.time.slots]:
                return False, "Occupato"
        return True, "Libero"
    def checkStatusLockerAtTimeSlot(self,locker:Locker,date:date,slot:int)->int and Gender:
        matched_bookings = [b for b in self.bookings.values() if locker.name in [l.locker.name for l in b.lockers_usage] and slot in [i.number for i in b.time.slots] and b.time.day == date and b.state in (BookingState.REGISTERED,BookingState.IN_PROGRESS,BookingState.COMPLETED)]
        gender = None
        count = 0
        for b in matched_bookings:
            for lu in b.lockers_usage:
                if lu.locker.name == locker.name:
                    count += lu.players
                    #print(count)
                    #print(lu.gender,gender)
                    if gender is None:
                        #print("none")
                        gender = lu.gender
                        #print(gender)
        if count==0:
            gender = locker.gender
        return f"{count}/{locker.capacity} {gender.value}"

    def checkAvailabilityField(self, name: str, date: date, timeSlot: int):
        requested_slots = TIME_SLOTS[timeSlot:timeSlot + 3]
        requested_start = requested_slots[0].startTime
        requested_end = requested_slots[2].endTime
        matched_bookings = [book for book in self.bookings.values()
        if book.field.name == name and book.time.day == date and book.state in (BookingState.REGISTERED,BookingState.IN_PROGRESS)]
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
            if b.field.name == name and b.time.day == date and b.state in (BookingState.REGISTERED,BookingState.IN_PROGRESS, BookingState.COMPLETED)
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
        preferred_lockers = [l for l in lockersList if gender == l.gender and l.type == LockerType.MAIN]
        support_lockers = [l for l in lockersList if l.type == LockerType.SECONDARY]
        individual_lockers = [l for l in lockersList if l.type == LockerType.INDIVIDUAL]

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

        #print(f"spo prefe: {preferred_lockers}")
        #print(f"spo suppo: {support_lockers}")
        #print(f"spo indivi: {individual_lockers}")

        def compute_locker_usage(lock: Locker) -> tuple[int, set[Gender]]:
            usage = 0
            genders = set()
            for b in active_bookings:
                booking_slots = b.time.slots
                if not booking_slots:
                    continue

                booking_start = booking_slots[0].startTime
                booking_end = booking_slots[-1].endTime
                #print(f"CHECK: {booking_start} {booking_end}")
                if not (requested_end <= booking_start or requested_start >= booking_end):
                    for u in b.lockers_usage or []:
                        if u.locker.name == lock.name:
                            usage += u.players
                            genders.add(u.gender)
                            break  # conta solo una volta per booking-locker (altrimenti conta x3 fasce)
            return usage, genders

        def allocate_from_list(locker_list: List[Locker]) -> int:
            nonlocal n_players
            for lock in locker_list:
                used, genders = compute_locker_usage(lock)
                #print(f"Nome: {lock.name} Usati: {used} Generi: {genders}")
                #print(f"CHECK: Genere:{type(gender)}:{gender}, {genders}")
                if lock.type in (LockerType.SECONDARY,
                                 LockerType.INDIVIDUAL) and genders and gender not in genders:
                    #print("Spogliatoio occupato da genere diverso, salto")
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

        #print(f"Da allocare: {n_players} {gender}")
        remaining = allocate_from_list(preferred_lockers)
        #print(f"Rimanenti dopo MAIN: {remaining}")
        if remaining > 0:
            remaining = allocate_from_list(support_lockers)
        if remaining > 0:
            remaining = allocate_from_list(individual_lockers)

        if remaining > 0:
            #print("ERRORE: Spazio insufficiente")
            return []

        #for assi in assigned:
        #    print(f"Assegnato: {assi.locker.name} {assi.players} {assi.gender}")
        #print("\n\n")
        return assigned


    def getFavoriteSport(self,player:Player):
        dict = {}
        for b in self.bookings.values():
            if b.state in (BookingState.REGISTERED,BookingState.COMPLETED,BookingState.IN_PROGRESS) and b.player==player:
                if b.sport in dict:
                    dict[b.sport] += 1
                else:
                    dict[b.sport] = 1
        if len(list(dict.keys()))==0:
            return "/"
        return max(dict,key=dict.get).value

    def getFavoriteTime(self,player:Player):
        dict:Dict[TIME_SLOTS,int] = {}
        for b in self.bookings.values():
            if b.state in (BookingState.REGISTERED,BookingState.COMPLETED,BookingState.IN_PROGRESS) and b.player==player:
                for TS in b.time.slots:
                    if TS in dict:
                        dict[TS]+=1
                    else:
                        dict[TS] = 1
        if len(dict.keys())==0:
            return "/"
        return max(dict,key=dict.get).getAllTime()

    def getAvgPersonForBooking(self,player:Player):
        sum = 0
        nB = 0
        for b in self.bookings.values():
            if b.state in (BookingState.REGISTERED,BookingState.COMPLETED,BookingState.IN_PROGRESS) and b.player==player:
                sum+=b.totalPlayers
                nB+=1
        if nB==0:
            return "/"
        return sum//nB

    def generate_plot_avg_age_all_fields(self,year:int):
        month = ["Gen","Feb","Mar","Apr","Mag","Giu","Lug","Ago","Set","Ott","Nov","Dic"]
        bookings_map = {}       #month -> list(total age, n players)
        for m in range(12):
            bookings_map[m] = [0,0]
        for b in list(self.bookings.values()):
            if b.time.day.year != year:
                continue
            bookings_map[b.time.day.month][0] += b.totalPlayers*b.player.get_age(b.time.day)
            bookings_map[b.time.day.month][1] += b.totalPlayers
        values = [bookings_map[month][0]//bookings_map[month][1] if bookings_map[month][1] != 0 else 0 for month in bookings_map]
        fig, ax = plt.subplots(figsize=(7,7))
        fig.subplots_adjust()
        ax.plot(month,values,c = "#E30613")
        plt.xlabel("Mese")
        plt.ylabel("Valore")
        plt.xticks(rotation=45)
        buf = BytesIO()
        fig.savefig(buf, format='png',dpi=300)
        buf.seek(0)
        plt.close(fig)
        qimg = QImage()
        qimg.loadFromData(buf.getvalue(), 'PNG')
        pixmap = QPixmap.fromImage(qimg)
        return pixmap

    def generate_plot_total_genders_all_fields(self,year:int):
        months = ["Gen","Feb","Mar","Apr","Mag","Giu","Lug","Ago","Set","Ott","Nov","Dic"]
        bookings_map = {}  #month -> [M,F]
        for m in range(12):
            bookings_map[m] = [0,0]
        for b in list(self.bookings.values()):
            if b.time.day.year != year:
                continue
            bookings_map[b.time.day.month][0] += b.male
            bookings_map[b.time.day.month][1] += b.female
        fig, ax = plt.subplots(figsize=(7, 7))
        fig.subplots_adjust()
        ax.plot(months, [a[0] for a in list(bookings_map.values())], c="#00d0ff",label="Maschi")
        ax.plot(months, [a[1] for a in list(bookings_map.values())], c="#f772b7",label="Femmine")
        plt.xlabel("Mese")
        plt.ylabel("Numero Giocatori")
        ax.legend(title="Sesso")
        plt.xticks(rotation=45)
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=300)
        buf.seek(0)
        plt.close(fig)
        qimg = QImage()
        qimg.loadFromData(buf.getvalue(), 'PNG')
        pixmap = QPixmap.fromImage(qimg)
        return pixmap

    def generate_top5_fields(self,year:int):
        colors = [
            "#1f77b4",
            "#ff7f0e",
            "#2ca02c",
            "#d62728",
            "#9467bd",
            "#8c564b",
            "#e377c2",
            "#7f7f7f",
            "#bcbd22",
            "#17becf"
        ]
        months = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]
        bookings_map = {}  # month -> {Field-name,Total Hours}
        setNames = set(b.field.name for b in list(self.bookings.values()))
        tracker = {}
        for m in range(12):
            bookings_map[m] = {}
            for name in setNames:
                bookings_map[m][name] = 0
        for name in setNames:
            tracker[name] = 0
        #print(bookings_map)
        for b in list(self.bookings.values()):
            if b.time.day.year != year:
                continue
            bookings_map[b.time.day.month][b.field.name] += 1.5
            tracker[b.field.name] +=1.5         #save the total hours

        #get TOP 5
        top5_field_names = list(dict(sorted(tracker.items(), key=lambda x: x[1], reverse=True)[:5]).keys())

        fig, ax = plt.subplots(figsize=(7, 7))
        fig.subplots_adjust()
        for i in range(len(top5_field_names)):
            ax.plot(months, [a[top5_field_names[i]] for a in list(bookings_map.values())], c=colors[i],label=top5_field_names[i])
        plt.xlabel("Mese")
        plt.ylabel("Ore Prenotate")
        plt.xticks(rotation=45)
        ax.legend(title="Campi")
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=300)
        buf.seek(0)
        plt.close(fig)
        qimg = QImage()
        qimg.loadFromData(buf.getvalue(), 'PNG')
        pixmap = QPixmap.fromImage(qimg)
        return pixmap

    def generate_earning_trend(self,year:int):
        months = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]
        bookings_map = {}  # month -> total earn
        for m in range(12):
            bookings_map[m] = 0
        for b in list(self.bookings.values()):
            if b.time.day.year != year:
                continue
            bookings_map[b.time.day.month] += b.price
        print(bookings_map)
        fig, ax = plt.subplots(figsize=(7, 7))
        fig.subplots_adjust()
        ax.plot(months, [bookings_map[m] for m in range(12)], c="#E30613")
        plt.xlabel("Mese")
        plt.ylabel("Valore")
        plt.xticks(rotation=45)
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=300)
        buf.seek(0)
        plt.close(fig)
        qimg = QImage()
        qimg.loadFromData(buf.getvalue(), 'PNG')
        pixmap = QPixmap.fromImage(qimg)
        return pixmap



