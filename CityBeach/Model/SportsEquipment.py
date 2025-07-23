import datetime
from Model import EquipmentType
from Model import SportsCategory

class SportsEquipment:
    def __init__(self, id: int, name: str, equipmentType: EquipmentType.EquipmentType, sportCategory: SportsCategory.SportsCategory):
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