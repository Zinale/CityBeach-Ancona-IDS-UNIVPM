import datetime
from typing import List
import datetime
from Model.Gender import Gender

class Player:
    def __init__(self, id:int,name:str = " ",surname:str=" ",phone:str ="+39 333 333 3333",
                 email:str="example@invalid.com",datebirth:datetime.date | None=None,
                 gender:Gender.Gender = "M/F",added_by: str = "admin",password: str=""):
        self.id = id
        self.name = name
        self.surname = surname
        self.birthday = datebirth
        self.phone = phone
        self.email = email
        if datebirth is None:
            self.birthday = datetime.date.today()
        self.gender = gender
        self.data_created = datetime.datetime.now()
        self.added_by = added_by

    def __str__(self):
        return f"Player: '{self.name}'\t'{self.surname}'\tid:{self.id}"
    def __repr__(self):
        return f"{self.id}' {self.name}' \t|\t '{self.surname}' \t|\t '{self.phone}' \t|\t '{self.email}')\n\r"

