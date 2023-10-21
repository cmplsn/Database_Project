import bcrypt
from flask_login import UserMixin
from sqlalchemy import *
from classes.user import User


# classe Admin collegata a nostro DB
class Admin(User, UserMixin):
    __tablename__ = 'ADMIN'
    userUuid = Column(ForeignKey("USERS.uuid", ondelete='CASCADE'), primary_key=True)
    password = Column(Text, nullable=False)

    def __init__(self, name: str, surname: str, email: str, password: str, dateofbirth: DateTime, uuid: UUID = null):
        super().__init__(name, surname, email, dateofbirth, uuid)
        pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.password = pwd.decode('utf-8')

    def auth_pwd(self, pwd: str):
        return bcrypt.checkpw(pwd.encode('utf-8'), self.password.encode('utf-8'))

    def toJSON(self):
        return {'uuid': str(super().uuid),
                'name': super().name,
                'surname': super().surname,
                'email': super().email,
                'dateofbirth': str(super().dateofbirth)}

    def __repr__(self):
        return (f"Admin(userUuid:{self.uuid},name = '{self.name}', surname='{self.surname}',"
                f"email:{self.email}, password='***', dateofbirt={self.dateofbirth},uuid={self.uuid})")
