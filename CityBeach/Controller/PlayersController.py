from typing import List, Dict

import PyQt6.QtCore

from Model.Gender import Gender
from Model.Player import Player

class AppPlayersController:
    def __init__(self, players: Dict[int, Player],player_id:int):
        self.players = players
        self.player_id = player_id
        self.current_user = None

    def register_player(self,data,current_user) -> bool and int:
        try:
            name = data[0]
            surname = data[1]
            birthday = data[2]
            date = birthday.strip().split("/")
            if PyQt6.QtCore.QDate(int(date[2]),int(date[1]),int(date[0])) >= PyQt6.QtCore.QDate.currentDate():
                return False,1
            if current_user is None:
                return False, 2
            gender = data[3]
            phone = data[4]
            email = data[5]
            city = data[6]
            if "@" not in email:
                return False, 3
            if self.checkEmail(email):
                return False, 4
            if self.checkPhone(phone):
                return False,5
            self.player_id+=1
            self.players[self.player_id] = Player(
                self.player_id,name=name,surname=surname,datebirth=birthday,gender=gender,
                phone=phone,email=email, residence=city,added_by=current_user.username
            )
            return True,0
        except:
            return False,-1

    def delete_player(self,player:Player)->bool and int:
        try:
            if player:
                del self.players[player.id]
                return True,0
            else:
                return False,2
        except:
            return False, 1

    def edit_player(self,data,id_player_to_edit:int)-> bool and int:
        try:
            name = data[0]
            surname = data[1]
            birthday = data[2]
            date = birthday.strip().split("/")
            if PyQt6.QtCore.QDate(int(date[2]),int(date[1]),int(date[0])) >= PyQt6.QtCore.QDate.currentDate():
                return False,1
            gender = data[3]
            phone = data[4]
            email = data[5]
            city = data[6]
            if "@" not in email:
                return False, 2
            if self.checkEmail(email):
                return False, 3
            if self.checkPhone(phone):
                return False,4
            self.players[id_player_to_edit].name = name
            self.players[id_player_to_edit].surname = surname
            self.players[id_player_to_edit].birthday = birthday
            self.players[id_player_to_edit].gender = gender
            self.players[id_player_to_edit].phone = phone
            self.players[id_player_to_edit].email = email
            self.players[id_player_to_edit].residence = city
            return True,0
        except:
            return False,-1

    def checkPhone(self,phone:str):
        return any(getattr(player, "phone", None) == phone for player in self.players)

    def checkEmail(self,email:str):
        return any(getattr(player, "email", None) == email for player in self.players)

    def findByEmail(self,emaiL:str)->Player:
        return next((player for player in self.players.values() if player.email == emaiL), None)

