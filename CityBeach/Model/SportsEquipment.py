import datetime
from Model import EquipmentType

class SportsEquipment:
    def __init__(self, id: int, name: str, equipmentType: EquipmentType.EquipmentType, quantity: int):
        self.name = name
        self.equipmentType = equipmentType
        self.quantity = quantity
        self.date_added = datetime.datetime.now()

    def __str__(self):
        return f"Name: '{self.name}', Equipment Type: '{self.equipmentType}', Quantity: {self.quantity}, Date Added: {self.date_added}"
    def __repr__(self):
        return f"SportsEquipment(name='{self.name}', equipment_type='{self.equipmentType}', quantity={self.quantity}, date_added={self.date_added})"