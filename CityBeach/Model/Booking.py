import datetime
from datetime import *
from enum import Enum
from typing import List

from Model.User import User
from Model.Field import Field
from Model.Locker import LockerRoomUsage
from Model.Player import Player


class TimeSlot:
    def __init__(self,number:int,startTime:time,endTime:time):
        self.number = number
        self.startTime = startTime
        self.endTime = endTime

    def __str__(self):
        return f"Fascia Oraria '{self.number}': {self.startTime}-{self.endTime}"
    def __repr__(self):
        return f"Fascia Oraria '{self.number}': {self.startTime}-{self.endTime}"

class DayTimeSlot:
    def __init__(self,day:date,slot:(TimeSlot,TimeSlot,TimeSlot)):
        self.day = day
        self.slot = slot

    def getAllTime(self):
        return self.slot[0].startTime + "-" + self.slot[2].endTime
    def __str__(self):
        return f"Giorno: '{self.day}'. {self.slot}"
    def __repr__(self):
        return f"Giorno: '{self.day}'. {self.slot}"

class BookingState(Enum):
    REGISTERED = "Registrata"
    IN_PROGRESS = "In corso"
    CANCELLED = "Annullata"

#Stato, data_created, registrata da
class Booking:
    def __init__(self,field:Field,nPlayers:int,nMale:int,nFemale:int,
                 player:Player,when:DayTimeSlot,price:int,lockers_usage:List[LockerRoomUsage],id_booking:int,usr_added_by:User):
        self.price:int=price
        self.field = field
        self.totalPlayers = nPlayers
        self.male:int = nMale
        self.female:int = nFemale
        self.player = player
        self.time = when
        self.lockers_usage = lockers_usage
        self.id = id_booking
        self.data_created = datetime.datetime.now()
        self.state:BookingState=BookingState.REGISTERED
        self.registered_by:User=usr_added_by


