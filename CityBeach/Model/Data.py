import pickle
from encodings.punycode import selective_find
from typing import Dict

from Model.Article import Article
from Model.User import User


class AppData:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.articles: Dict[str, Article] = {}
        self.current_user: User | None = None

    def save_to_file(self, path: str):
        with open(path, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load_from_file(path: str) -> "AppData":
        try:
            with open(path, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return AppData()