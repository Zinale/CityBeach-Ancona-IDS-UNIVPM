from enum import Enum

class FieldType(Enum):
    PADEL = "Padel"
    BEACH = "Beach"

class BeachSportsType(Enum):
    BEACH_TENNIS = "Beach Tennis"
    BEACH_VOLLEY = "Beach Volley"

class Sports(Enum):
    PADEL = "Padel"
    BEACH_TENNIS = "Beach Tennis"
    BEACH_VOLLEY = "Beach Volley"