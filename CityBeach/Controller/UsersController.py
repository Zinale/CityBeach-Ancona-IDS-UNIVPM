from types import UnionType
from typing import List, Dict

import PyQt6.QtCore
from Model.Gender import Gender
from Model.User import User

class AppUsersController:
    def __init__(self, users: Dict[int, User],user_id:int):
        self.users = users
        self.user_id = user_id
        self.current_user:User|None = None
    def __str__(self):
        return f"AppUsersController, utente attivo:{self.current_user.username}"
    def register(self,data,password:str="") -> bool and int:
        try:
            if self.current_user is not None and not self.current_user.is_admin:
                return False, 6
            name = data["name"].strip()
            surname = data["surname"].strip()
            username = data["username"].strip()
            if not name.isalnum():
                return False, 1
            if not surname.isalnum():
                return False, 2
            usernames = [p.username for p in self.get_all_users()]
            if username in usernames:
                return False, 3
            if not username.isalnum():
                return False, 4
            birthday = data["birthday"]
            date= birthday.split("/")
            if PyQt6.QtCore.QDate(int(date[2]),int(date[1]),int(date[0])) >= PyQt6.QtCore.QDate.currentDate():
                return False, 5
            gender = data["gender"]
            is_admin = data["is_admin"]
            if self.current_user is not None:
                addedBy = self.current_user.username
            else:
                addedBy = "root"
            self.user_id+=1
            self.users[self.user_id] = User(self.user_id,username=username, is_admin=is_admin,name=name,surname=surname,
                                              datebirth=birthday,gender=gender,added_by=addedBy,password=password)
            return True, 0
        except Exception as e:
            print(e)
            return False, -1

    def login(self, username: str, password: str)-> bool:
        for user in self.get_all_users():
            if user.username == username and user.password == password:
                self.current_user = user
                return True
        return False

    def delete_user(self,user:User)->bool and int:
        try:
            current_user = self.current_user
            if not current_user or not current_user.is_admin:
                return False, 2
            user_to_delete = user
            if current_user.username == user_to_delete.username:
                return False, 1
            if user_to_delete:
                id_to_delete = user_to_delete.id
                del self.users[id_to_delete]
                return True, 0
        except Exception:
            return False, 3

    def edit_user(self,user_id,new_name,new_surname,new_username,new_password,new_birthday,new_gender) -> bool and int:
        try:
            new_name = new_name.strip()
            new_surname = new_surname.strip()
            new_username = new_username.strip()
            if not new_name.isalnum():
                return False, 1
            if not new_surname.isalnum():
                return False, 2
            usernames = [p.username for p in self.get_all_users()]
            if new_username in usernames and new_username!=self.users[user_id].username:
                return False, 3
            if not new_username.isalnum():
                return False, 4
            date = new_birthday.split("/")
            if PyQt6.QtCore.QDate(int(date[2]), int(date[1]), int(date[0])) >= PyQt6.QtCore.QDate.currentDate():
                return False, 5
            if user_id == 1:
                return False, 6 #can't edit "admin" (root) profile
            self.users[user_id].name = new_name
            self.users[user_id].surname = new_surname
            self.users[user_id].username = new_username
            if type(new_password) == str:
                self.users[user_id].password = new_password
            elif type(new_password) == bool:        #admins can just reset password of other accounts
                if new_password:
                    self.users[user_id].password = ""
            self.users[user_id].birthday = new_birthday
            self.users[user_id].gender = new_gender
            return True, 0
        except Exception:
            return False, 0

    def logout(self) -> bool:
        try:
            self.current_user = None
            return True
        except Exception as e:
            return False

    def get_id_by_username(self,username:str)->int:
        return next(id for id, user in self.get_all_users() if user.username == username)
    def get_user_by_username(self,username:str)->User | None:
        return next((user for user in self.get_all_users() if user.username == username),None)
    def get_current_user(self)->User|None:
        return self.current_user
    def get_all_users(self) -> List[User] :
        return list(self.users.values())

    def __str__(self):
        return f"User Controller!"