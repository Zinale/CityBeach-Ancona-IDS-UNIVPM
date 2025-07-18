from typing import Dict
from Model.Locker import Locker

class AppLockersController:
    def __init__(self, lockers: Dict[int, Locker], locker_id: int):
        self.lockers = lockers
        self.locker_id = locker_id

    def register_locker(self,data,usr)->bool and int:
        try:
            name = data["name"].strip()
            if len(name) == 0:
                return False, 1
            gender = data["gender"].value
            capacity = int(data["capacity"])
            if capacity < 0:
                return False, 2
            self.locker_id+=1
            self.lockers[self.locker_id] = Locker(self.locker_id,name,gender,capacity,usr)
            return True, 0
        except:
            return False, -1
    def edit_locker(self,data,id_locker_to_edit:int)-> bool and int:
        try:
            name = data["name"]
            if len(name) == 0:
                return False, 1
            self.lockers[id_locker_to_edit].name = name
            self.lockers[id_locker_to_edit].capacity = data["capacity"]
            self.lockers[id_locker_to_edit].gender = data["gender"].value
            return True, 0
        except:
            return False, -1

    def delete_locker(self,locker_to_delete:Locker)-> bool and int:
        try:
            if locker_to_delete:
                del self.lockers[locker_to_delete.id]
                return True, 0
            else:
                return False, 2
        except:
            return False, 1
