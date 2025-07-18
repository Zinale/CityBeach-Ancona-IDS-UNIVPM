import datetime
from Model.SportsCategory import SportsCategory

class Field:
    def __init__(self, id:int,sport:SportsCategory,name:str,usr_added_by:str):
        self.id = id
        self.name = name
        self.sport:SportsCategory = sport
        self.data_created:datetime = datetime.datetime.now()
        self.added_by = usr_added_by

    def __str__(self):
        return f"Field: '{self.id}'\t'{self.name}'\tsport:{type(self.sport)}{self.sport}\tadded by:{self.added_by}"
    def __repr__(self):
        return f"{self.id}'\t'{self.name}'\tid:{self.sport}\tadded by:{self.added_by}')\n\r"
