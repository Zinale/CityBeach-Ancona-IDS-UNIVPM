from types import new_class
from typing import List, Dict

import PyQt6.QtCore
from Model.Data import AppData
from Model.SportsEquipment import SportsEquipment
from Model.EquipmentType import EquipmentType

class AppSportsEquipmentController:
    def __init__(self, equipment: Dict[int, SportsEquipment], equipment_id: int):
        self.equipment = equipment
        self.equipment_id = equipment_id

    def get_all_equipment(self) -> List[SportsEquipment]:
        return list(self.equipment.values())
    
    def add_equipment(self, name: str, equipmentType: EquipmentType, quantity: int) -> bool and int:
        try:
            name = name.strip()
            equipmentType = equipmentType.strip()
            if not name.isalnum():
                return False, 1
            if isinstance(equipmentType, EquipmentType):
                return False, 2
            if quantity <= 0:
                return False, 3
            
            self.equipment_id += 1
            self.equipment[self.equipment_id] = SportsEquipment(
                id=self.equipment_id,
                name = name,
                equipmentType = equipmentType,
                quantity = quantity
            )
            return True, 0
        except:
            return False, -1