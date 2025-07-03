import datetime

class SportsEquipment:
    def __init__(self, id: int, name: str, sport_type: str, quantity: int):
        self.name = name
        self.sport_type = sport_type
        self.quantity = quantity
        self.date_added = datetime.datetime.now()

    def __str__(self):
        return f"Name: '{self.name}', Sport Type: '{self.sport_type}', Quantity: {self.quantity}, Date Added: {self.date_added}"
    def __repr__(self):
        return f"SportsEquipment(name='{self.name}', sport_type='{self.sport_type}', quantity={self.quantity}, date_added={self.date_added})"