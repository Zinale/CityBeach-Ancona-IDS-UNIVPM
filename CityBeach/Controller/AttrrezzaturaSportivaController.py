from types import new_class
from typing import List, Dict

import PyQt6.QtCore
from Model.Data import AppData
from Model.SportsEquipment import SportsEquipment
from Model.SportsEquipment import *
from Model.SportsCategory import *

class AppSportsEquipmentController:
    def __init__(self, equipment: Dict[int, SportsEquipment] = None):
        self.equipment = equipment
        #self.equipment_id = equipment_id

    def get_all_equipment(self) -> List[SportsEquipment]:
        return list(self.equipment.values())
    
    def get_equipment_by_id(self, equipment_id: int) -> SportsEquipment:
        return self.equipment.get(equipment_id, None)
    
    def modify_quantity(self, equipment_id: int, new_quantity: int) -> bool:
        if new_quantity >= 0:
            self.equipment[equipment_id].quantity = new_quantity
            return True
        return False