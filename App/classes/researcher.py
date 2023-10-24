import bcrypt
from flask_login import UserMixin
from sqlalchemy import *
from sqlalchemy.orm import relationship
from classes.authors import authors
from classes.user import User


class Researcher(User, UserMixin):
    __tablename__ = 'RESEARCHERS'
    userUuid = Column(ForeignKey("USERS.uuid", ondelete='CASCADE'), primary_key=True)
    password = Column(String, nullable=False)
    cv = Column(LargeBinary)
    authors = relationship("Project", secondary=authors, back_populates='RESEARCHERS')
    messages = relationship("Messages")
    versions = relationship("Versions")

    def __init__(self,  name: str, surname: str, email: str, password: str, cv: LargeBinary, dateofbirth: DateTime,
                 uuid: UUID = null):
        super().__init__(name, surname, email, dateofbirth, uuid)
        pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.password = pwd.decode('utf-8')
        self.cv = cv

    def auth_pwd(self, pwd: str):
        return bcrypt.checkpw(pwd.encode('utf-8'), self.password.encode('utf-8'))

    def toJSON(self):
        return {'uuid': str(super().uuid),
                'name': super().name,
                'surname': super().surname,
                'email': super().email,
                'dateofbirth': super().dateofbirth,
                'cv': self.cv}

    def __repr__(self):
        return (f"Researcher(userUuid:{self.userUuid}, name='{self.name}', surname='{self.surname}'"
                f"email='{self.email}', password='***', dateofbirth={self.dateofbirth}, uuid={self.uuid}")
