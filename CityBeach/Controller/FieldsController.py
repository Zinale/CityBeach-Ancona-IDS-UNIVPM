from typing import Dict
from Model.Field import Field

class AppFieldsController:
    def __init__(self, fields: Dict[int, Field], field_id: int):
        self.fields = fields
        self.field_id = field_id