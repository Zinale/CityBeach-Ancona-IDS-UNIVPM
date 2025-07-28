import datetime
from enum import Enum
from Model import SportsCategory

class EquipmentType(Enum):
    PADEL_RACKETS = "Racchetta da Padel"
    PADEL_BALLS = "Pallina da Padel"
    BEACH_TENNIS_RACKETS = "Racchetta da Beach Tennis"
    BEACH_TENNIS_BALLS = "Pallina da Beach Tennis"
    BEACH_VOLLEYBALLS = "Palla da Beach Volley"

class SportsEquipment:
    def __init__(self, id: int, name: str, equipmentType: EquipmentType, sportCategory: SportsCategory.FieldType):
        self.id = id
        self.name = name
        self.equipmentType = equipmentType
        self.sportCategory = sportCategory
        self.quantity = 0
        self.date_added = datetime.datetime.now()

    def __str__(self):
        return f"Name: '{self.name}', Equipment Type: '{self.equipmentType}', Quantity: {self.quantity}, Date Added: {self.date_added}"
    def __repr__(self):
        return f"SportsEquipment(name='{self.name}', equipment_type='{self.equipmentType}', quantity={self.quantity}, date_added={self.date_added})"
    