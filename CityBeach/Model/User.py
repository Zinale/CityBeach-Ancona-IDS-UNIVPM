import datetime
from typing import List

from Model.Gender import Gender
import datetime


class User:
    def __init__(self, id:int,username: str, is_admin:bool = False,
                 name:str = " ",surname:str=" ",datebirth:datetime.date | None=None,added_by: str = "admin",password: str="",gender:Gender = Gender.OTHER):
        self.id = id
        self.username = username
        self.password = password
        self.name = name
        self.surname = surname
        self.birthday = datebirth
        if datebirth is None:
            self.birthday = datetime.date.today()
        self.gender = gender
        self.is_admin:bool = False
        if is_admin:
            self.is_admin = True

        self.data_created = datetime.datetime.now()
        self.added_by = added_by

    def __str__(self):
        return f"Username: '{self.username}'\t\t\t\tPassword: '{self.password}'\tid:{self.id}"
    def __repr__(self):
        return f"{self.id}' {self.username}' \t|\t '{self.password}' \t|\t '{self.is_admin}' \t|\t '{self.data_created}')\n\r"


