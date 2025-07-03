from types import new_class
from typing import List, Dict

import PyQt6.QtCore
from Model.Data import AppData
from Model.SportsEquipment import SportsEquipment

class AppSportsEquipmentController:
    def __init__(self, equipment: Dict[int, SportsEquipment], equipment_id: int):
        self.equipment = equipment
        self.equipment_id = equipment_id
        print(equipment)

    def get_all_equipment(self) -> List[SportsEquipment]:
        return list(self.equipment.values())