import datetime
from typing import List

from Model.Article import Article
import datetime


class User:
    def __init__(self, username: str, password: str, is_admin:bool = False,
                 name:str = " ",surname:str=" ",datebirth:datetime.date | None=None,
                 sesso:str = "M/F",added_by: str = "admin"):
        self.username = username
        self.password = password
        self.name = name
        self.surname = surname
        self.birthday = datebirth
        if datebirth is None:
            self.birthday = datetime.date.today()
        self.sesso = sesso
        self.article_ids: List[str] = []
        self.is_admin:bool = False
        if is_admin:
            self.is_admin = True

        self.data_created = datetime.datetime.now()
        self.added_by = added_by

    def __str__(self):
        return f"Username: '{self.username}'\t\t\t\tPassword: '{self.password}'"
    def __repr__(self):
        print("USERNAME\t|\tPASSWORD\t|\tis_admin\t|\tDATETIME_created")
        return f"'{self.username}' \t|\t '{self.password}' \t|\t '{self.is_admin}' \t|\t '{self.data_created}')"

    def can_delete(self, article: Article) -> bool:
        return article.id in self.article_ids

