from sqlalchemy import Column, Integer, String
from features import db, Hash


class User(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(150), unique=True, nullable=False)
    password = Column(String(250), nullable=True)

    def __init__(self, username, password=None):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User {self.username}>"

    def check_password(self, password_given: str):
        return Hash.are_equals(self.password, password_given)

    def encrypt_password(self):
        self.password = Hash.encrypt(self.password)