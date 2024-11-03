from .model import User
from features import db


class UserCU:
    def __init__(self):
        self.db = db

    def get_user(self, username) -> User | None:
        return self.db.session.query(User).filter_by(username=username).first()

    def create_user(self, username, password) -> User | None:
        if self.get_user(username):
            return None
        else:
            user = User(username=username, password=password)
            user.encrypt_password()
            self.db.session.add(user)
            self.db.session.commit()
            return user

    def create_user_without_password(self, username) -> User | bool:
        if self.get_user(username):
            return True
        else:
            user = User(username=username)
            self.db.session.add(user)
            self.db.session.commit()
            return user
