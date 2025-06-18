from typing import List

from Model.Article import Article


class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.article_ids: List[str] = []
    def __str__(self):
        return f"Username: '{self.username}'\t\t\t\tPassword: '{self.password}'"
    def __repr__(self):
        return f"{self.username}:\t {self.password})"

    def can_delete(self, article: Article) -> bool:
        return article.id in self.article_ids

class Amministratore(User):
    def __init__(self):
        super().__init__()
