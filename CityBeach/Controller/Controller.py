from typing import List

from Model.Article import Article
from Model.Data import AppData
from Model.User import User

class AppController:
    def __init__(self, model: AppData):
        self.model = model

    def login(self, username: str, password: str) -> bool:
        user = self.model.users.get(username)
        if user and user.password == password:
            self.model.current_user = user
            return True
        return False

    def register(self, username: str, password: str,is_admin:bool = False) -> bool:
        if username in self.model.users:
            return False
        self.model.users[username] = User(username, password)
        return True

    def logout(self):
        self.model.current_user = None
        self.model.save_to_file("data.pkl")

    def add_article(self, title: str) -> bool:
        user = self.model.current_user
        if not user:
            return False
        article = Article(title, user.username)
        self.model.articles[article.id] = article
        user.article_ids.append(article.id)
        return True

    def delete_article(self, article_id: str) -> bool:
        user = self.model.current_user
        if not user:
            return False
        article = self.model.articles.get(article_id)
        if article and user.can_delete(article):
            del self.model.articles[article_id]
            user.article_ids.remove(article_id)
            return True
        return False

    def modifica_user(self, new_username, new_password):
        user = self.model.current_user
        if not user:
            return False
        if new_username != user.username:
            self.model.users[new_username] = self.model.users.pop(user.username)
            for art_id in user.article_ids:
                self.model.articles[art_id].owner = new_username

        user.username = new_username
        user.password = new_password
        self.model.save_to_file('data.pkl')

        return True





    def get_all_articles(self) -> List[Article]:
        return list(self.model.articles.values())

    def get_current_user(self) -> User | None:
        return self.model.current_user