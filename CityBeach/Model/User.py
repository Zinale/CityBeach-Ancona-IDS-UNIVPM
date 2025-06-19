import datetime
from typing import List

from Model.Article import Article
from datetime import *


class User:
    def __init__(self, username: str, password: str, is_admin:bool = False):
        self.username = username
        self.password = password
        self.data_created = datetime.now()
        self.article_ids: List[str] = []
        self.is_admin:bool = False
        if is_admin:
            self.is_admin = True

    def __str__(self):
        return f"Username: '{self.username}'\t\t\t\tPassword: '{self.password}'"
    def __repr__(self):
        print("USERNAME\t|\tPASSWORD\t|\tis_admin\t|\tDATETIME_created")
        return f"'{self.username}' \t|\t '{self.password}' \t|\t '{self.is_admin}' \t|\t '{self.data_created}')"

    def can_delete(self, article: Article) -> bool:
        return article.id in self.article_ids

