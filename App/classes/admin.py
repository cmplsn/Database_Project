import bcrypt
from flask_login import UserMixin
from sqlalchemy import *
from classes.user import User


# classe Admin collegata a nostro DB
class Admin(User, UserMixin):
    __tablename__ = 'ADMIN'
    userUuid = Column(ForeignKey("USERS.uuid", ondelete='CASCADE'), primary_key=True)
    password = Column(Text, nullable=False)

    def __init__(self, name: str, surname: str, email: str, password: str, dateofbirth: DateTime, uuid: UUID = null,):
        super().__init__(name, surname, email, dateofbirth, uuid)

        pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())



