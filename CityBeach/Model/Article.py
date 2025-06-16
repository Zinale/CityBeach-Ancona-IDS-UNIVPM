import uuid
class Article:
    def __init__(self, title: str, owner: str):
        self.id = str(uuid.uuid4())
        self.title = title
        self.owner = owner

    def __repr__(self):
        return f"{self.title} (di {self.owner})"