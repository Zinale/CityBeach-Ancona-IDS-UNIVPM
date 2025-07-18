from typing import Dict
from Model.Field import Field
from Model.SportsCategory import SportsCategory


class AppFieldsController:
    def __init__(self, fields: Dict[int, Field], field_id: int):
        self.fields = fields
        self.field_id = field_id

    def register_field(self,data,usr:str | None)->bool and int:
        try:
            name = data["name"]
            sport = data["sport"]
            if usr is None:
                return False, 1
            if sport.value not in [sport.value for sport in SportsCategory]:
                return False, 2
            if len(name.strip()) <=0:
                return False,3
            self.field_id+=1
            self.fields[self.field_id] = Field(self.field_id,sport.value,name,usr)
            return True,0
        except:
            return False, -1

    def delete_field(self,field_to_delete:Field)-> bool and int:
        try:
            if field_to_delete:
                del self.fields[field_to_delete.id]
                return True, 0
            else:
                return False, 2
        except:
            return False, 1
