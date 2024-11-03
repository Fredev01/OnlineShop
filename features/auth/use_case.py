from .model import User
from features import db


class UserCU:
    def __init__(self, cb_generate_password_hash, cb_check_password_hash):
        self.db = db
        self.cb_generate_password_hash = cb_generate_password_hash
        self.cb_check_password_hash = cb_check_password_hash

    def set_password(self, user: User, password):
        user.password_hash = self.cb_generate_password_hash(password)

    def check_password(self, user: User, password):
        return self.cb_check_password_hash(user.password_hash, password)

    def get_user(self, username) -> User | None:
        return self.db.session.query(User).filter_by(username=username).first()

    def create_user(self, username, password) -> User | None:
        if self.get_user(username):
            return None
        else:
            user = User(username=username)
            self.set_password(user, password)
            self.db.session.add(user)
            self.db.session.commit()
            return user

