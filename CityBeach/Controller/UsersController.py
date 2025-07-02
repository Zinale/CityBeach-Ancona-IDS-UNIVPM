from types import new_class
from typing import List, Dict

import PyQt6.QtCore
from Model.Data import AppData
from Model.Gender import Gender
from Model.User import User

class AppUsersController:
    def __init__(self, users: Dict[int, User],user_id:int):
        self.users = users
        self.user_id = user_id
        self.current_user = None

    def register(self,name:str,surname:str,username:str,birthday,is_admin:bool,gender:Gender = Gender.OTHER,password:str = "") -> bool and int:
        try:
            name = name.strip()
            surname = surname.strip()
            username = username.strip()
            if not name.isalnum():
                return False, 1
            if not surname.isalnum():
                return False, 2
            usernames = [p.username for p in self.get_all_users()]
            if username in usernames:
                return False, 3
            if not username.isalnum():
                return False, 4
            date= birthday.split("/")
            if PyQt6.QtCore.QDate(int(date[2]),int(date[1]),int(date[0])) >= PyQt6.QtCore.QDate.currentDate():
                return False, 5

            if self.current_user != None:
                addedBy = self.current_user.username
            else:
                addedBy = "root"
            self.user_id+=1
            self.users[self.user_id] = User(self.user_id,username, is_admin=is_admin,name=name,surname=surname,
                                              datebirth=birthday,gender=gender,added_by=addedBy,password=password)
            return True, 0
        except:
            return False, -1

    def login(self, username: str, password: str):
        for user in self.get_all_users():
            if user.username == username and user.password == password:
                self.current_user = user
                return True, self.current_user
        return False, None

    def delete_user(self,username:str)->bool and int:
        try:
            current_user = self.current_user
            if not current_user or not current_user.is_admin:
                return False, 2
            user_to_delete = self.get_user_by_username(username)
            if current_user.username == user_to_delete.username:
                return False, 1
            if user_to_delete:
                id_to_delete = user_to_delete.id
                del self.users[id_to_delete]
                return True,0
        except:
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
            elif type(new_password) == bool:
                if new_password:
                    self.users[user_id].password = ""
            self.users[user_id].birthday = new_birthday
            self.users[user_id].gender = new_gender
            return True, 0
        except Exception:
            return False, 0

    def logout(self):
        self.current_user = None

#    def add_article(self, title: str) -> bool:
#        user = self.model.current_user
#        if not user:
#            return False
#        article = Article(title, user.username)
#        self.model.articles[article.id] = article
#        user.article_ids.append(article.id)
#        return True

 #   def delete_article(self, article_id: str) -> bool:
 #       user = self.model.current_user
 #       if not user:
 #           return False
 #       article = self.model.articles.get(article_id)
 #       if article and user.can_delete(article):
 #           del self.model.articles[article_id]
 #           user.article_ids.remove(article_id)
 #           return True
 #       return False
   # def get_all_articles(self) -> List[Article]:
   #     return list(self.model.articles.values())

    def get_id_by_username(self,username:str)->int:
        return next(id for id, user in self.get_all_users() if user.username == username)
    def get_user_by_username(self,username:str)->User | None:
        return next((user for user in self.get_all_users() if user.username == username),None)
    def get_current_user(self):
        return self.current_user
    def get_all_users(self) -> List[User] :
        return list(self.users.values())