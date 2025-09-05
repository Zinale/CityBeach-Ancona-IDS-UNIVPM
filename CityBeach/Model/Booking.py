from datetime import *
from enum import Enum
from typing import List

from Model.User import User
from Model.Field import Field
from Model.Locker import LockerRoomUsage
from Model.Player import Player
from Model.SportsCategory import *


class TimeSlot:
    def __init__(self,number:int,startTime:time,endTime:time):
        self.number = number
        self.startTime = startTime
        self.endTime = endTime

    def __str__(self):
        return f"Fascia Oraria: {self.startTime}-{self.endTime}"
    def __repr__(self):
        return f"Fascia Oraria '{self.number}': {self.startTime}-{self.endTime}"
    def getAllTime(self):
        return f"{self.startTime.strftime('%H:%M')}-{self.endTime.strftime('%H:%M')}"

class DayTimeSlot:
    def __init__(self,day:date,slot:(TimeSlot,TimeSlot,TimeSlot)):
        self.day = day
        self.slots = slot

    def getAllTime(self):
        return f"{self.slots[0].startTime.strftime('%H:%M')}-{self.slots[2].endTime.strftime('%H:%M')}"

    def __str__(self):
        return f"Giorno: '{self.day}'. {self.slots}"
    def __repr__(self):
        return f"Giorno: '{self.day}'. {self.slots}"

class BookingState(Enum):
    REGISTERED = "Registrata"
    IN_PROGRESS = "In corso"
    CANCELLED = "Annullata"
    COMPLETED = "Terminata"

#Stato, data_created, registrata da
class Booking:
    def __init__(self, field: Field, nPlayers: int, nMale: int, nFemale: int,
                 player: Player, when: DayTimeSlot, price: int=0,
                 id_booking: int=0, usr_added_by: User=None,
                 lockers_usage: List[LockerRoomUsage] = None, sport: Sports = None):
        self.price:int=price
        self.field = field
        self.totalPlayers = nPlayers
        self.male:int = nMale
        self.female:int = nFemale
        self.player = player
        self.time = when
        self.lockers_usage = lockers_usage
        self.id = id_booking
        self.data_created = datetime.now()
        self.state:BookingState=BookingState.REGISTERED
        self.registered_by:User=usr_added_by
        self.sport:Sports = sport
        self.se_list = []

    def __str__(self):
        return (f"Prenotazione: {self.id}\tGiocatore:{self.player.name}\tCampo:{self.field.name} x {self.field.sport}\n\r"
                f"{self.time}")