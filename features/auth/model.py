from sqlalchemy import Column, Integer, String
from features import db


class User(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(250), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"