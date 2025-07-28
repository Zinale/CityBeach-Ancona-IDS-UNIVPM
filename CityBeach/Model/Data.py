import pickle
from typing import Dict

from Model.Locker import Locker
from Model.SportsEquipment import *
from Model.Booking import *
from Model.SportsCategory import *

#all the time_slots available
TIME_SLOTS = []
for i in range(28):
    TIME_SLOTS.append(TimeSlot(number=i+1,
                               startTime=time(9 + i//2,30*((i)%2)),
                               endTime=time(9 + ((i+1)//2),30-30*((i)%2))))
TIME_SLOTS_str = [str(ts) for ts in TIME_SLOTS]

class AppData:
    def __init__(self):
        self.users: Dict[int, User] = {}
        self.users_next_id: int = 0
        self.current_user: User | None = None
        self.equipment:Dict[int,SportsEquipment] ={
            0: SportsEquipment(id=0, name="Racchetta da Padel", equipmentType=EquipmentType.PADEL_RACKETS, sportCategory=Sports.PADEL),
            1: SportsEquipment(id=1, name="Pallina da Padel", equipmentType=EquipmentType.PADEL_BALLS, sportCategory=Sports.PADEL),
            2: SportsEquipment(id=2, name="Racchetta da Beach Tennis", equipmentType=EquipmentType.BEACH_TENNIS_RACKETS, sportCategory=Sports.BEACH_TENNIS),
            3: SportsEquipment(id=3, name="Pallina da Beach Tennis", equipmentType=EquipmentType.BEACH_TENNIS_BALLS, sportCategory=Sports.BEACH_TENNIS),
            4: SportsEquipment(id=4, name="Palla da Beach Volley", equipmentType=EquipmentType.BEACH_VOLLEYBALLS, sportCategory=Sports.BEACH_VOLLEY)
        }
        self.equipment_next_id: int = 0
        self.players:Dict[int,Player] = {}
        self.players_next_id:int = 0
        self.fields:Dict[int,Field] = {}
        self.fields_next_id:int = 0
        self.lockers: Dict[int, Locker] = {}
        self.lockers_next_id: int = 0
        self.bookings:Dict[int,Booking] = {}
        self.bookings_next_id:int = 0

    def save_to_file(self, path: str):
        with open(path, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load_from_file(path: str) -> "AppData":
        try:
            with open(path, 'rb') as f:
                return pickle.load(f)
        except (FileNotFoundError,pickle.UnpicklingError):
            return AppData()