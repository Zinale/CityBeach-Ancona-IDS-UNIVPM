from types import new_class
from typing import List, Dict

import PyQt6.QtCore
from Model.Data import AppData
from Model.SportsEquipment import SportsEquipment
from Model.EquipmentType import EquipmentType
from Model.SportsCategory import SportsCategory

class AppSportsEquipmentController:
    def __init__(self):
        self.equipment = {
            1: SportsEquipment(id=0, name="Racchetta da Padel", equipmentType=EquipmentType.PADEL_RACKETS, sportCategory=SportsCategory.PADEL, quantity=0),
            2: SportsEquipment(id=1, name="Pallina da Padel", equipmentType=EquipmentType.PADEL_BALLS, sportCategory=SportsCategory.PADEL, quantity=0),
            3: SportsEquipment(id=2, name="Racchetta da Beach Tennis", equipmentType=EquipmentType.BEACH_TENNIS_RACKETS, sportCategory=SportsCategory.BEACH_TENNIS, quantity=0),
            4: SportsEquipment(id=3, name="Pallina da Beach Tennis", equipmentType=EquipmentType.BEACH_TENNIS_BALLS, sportCategory=SportsCategory.BEACH_TENNIS, quantity=0),
            5: SportsEquipment(id=4, name="Palla da Beach Volley", equipmentType=EquipmentType.BEACH_VOLLEYBALLS, sportCategory=SportsCategory.BEACH_VOLLEY, quantity=0)
        }
        #self.equipment_id = equipment_id

    def get_all_equipment(self) -> List[SportsEquipment]:
        return list(self.equipment.values())
    
    #def add_equipment(self, name: str, equipmentType: EquipmentType, sportsCategory: SportsCategory, quantity: int) -> bool and int:
        try:
            name = name.strip()
            equipmentType = equipmentType.strip()
            if not name.isalnum():
                return False, 1
            if isinstance(equipmentType, EquipmentType):
                return False, 2
            if isinstance(sportsCategory, SportsCategory):
                return False, 3
            if quantity <= 0:
                return False, 4
            
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