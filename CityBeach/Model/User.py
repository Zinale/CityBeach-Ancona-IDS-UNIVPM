from typing import List

from Model.Article import Article


class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.article_ids: List[str] = []

    def can_delete(self, article: Article) -> bool:
        return article.id in self.article_ids