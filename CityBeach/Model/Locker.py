import datetime
from Model.Gender import Gender

class Locker:
    def __init__(self, id:int,name:str,gender:Gender,capacity:int,usr_added_by:str):
        self.id = id
        self.name = name
        self.gender:Gender = gender
        self.capacity = capacity
        self.data_created = datetime.datetime.now()
        self.added_by = usr_added_by

    def __str__(self):
        return f"Locker Room: '{self.id}'\t'{self.name}'\tGender:{self.gender}\tCapacity:{self.capacity}\tadded by:{self.added_by}"
    def __repr__(self):
        return f"'{self.id}'\t'{self.name}'\tGender:{self.gender}\tCapacity:{self.capacity}\tadded by:{self.added_by})\n\r"

