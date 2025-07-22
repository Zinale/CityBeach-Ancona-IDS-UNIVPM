import datetime
import uuid
from enum import Enum

from Model.Gender import Gender
from Model.User import User


class LockerType(Enum):
    MAIN = "Principale"
    SECONDARY = "Secondario"
    INDIVIDUAL = "Individuale"

class Locker:
    def __init__(self, id:int,name:str,gender:Gender,lockerType:LockerType,capacity:int,usr_added_by:User):
        self.id = id
        self.name = name
        self.gender:Gender = gender
        self.capacity = capacity
        self.type = lockerType
        self.data_created = datetime.datetime.now()
        self.added_by = usr_added_by

    def getDetails(self):
        return f"Locker Room: '{self.id}'\t'{self.name}'\tGender:{self.gender}\tCapacity:{self.capacity}\tadded by:{self.added_by.username}"
    def __str__(self):
        return f"{self.name}"
    def __repr__(self):
        return f"{self.name}"
        return f"'{self.id}'\t'{self.name}'\tGender:{self.gender}\tCapacity:{self.capacity}\tadded by:{self.added_by.username})\n\r"


class LockerRoomUsage:
    def __init__(self,locker:Locker,players:int,gender:Gender):
        self.id_locker_usage = str(uuid.uuid4())
        self.locker = locker
        self.players = players
        self.gender = gender

    def __str__(self):
        return f"{self.id_locker_usage}"
    def __repr__(self):
        return f"{self.id_locker_usage}"