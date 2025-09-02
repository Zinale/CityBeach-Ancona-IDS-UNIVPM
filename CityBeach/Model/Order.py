import datetime
import uuid
from enum import Enum

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
