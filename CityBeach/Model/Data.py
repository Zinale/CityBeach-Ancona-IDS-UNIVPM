import pickle
from typing import Dict

from Model.Field import Field
from Model.Locker import Locker
from Model.Article import Article
from Model.Player import Player
from Model.User import User
from Model.SportsEquipment import SportsEquipment

class AppData:
    def __init__(self):
        self.users: Dict[int, User] = {}
        self.users_next_id: int = 0
        self.articles: Dict[str, Article] = {}
        self.current_user: User | None = None
        self.equipment:Dict[int,SportsEquipment] = {}
        self.equipment_next_id: int = 0
        self.players:Dict[int,Player] = {}
        self.players_next_id:int = 0
        self.fields:Dict[int,Field] = {}
        self.fields_next_id:int = 0
        self.lockers: Dict[int, Locker] = {}
        self.lockers_next_id: int = 0

    def save_to_file(self, path: str):
        with open(path, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load_from_file(path: str) -> "AppData":
        try:
            with open(path, 'rb') as f:
                return pickle.load(f)
        except (FileNotFoundError,pickle.UnpicklingError):
            return AppData()