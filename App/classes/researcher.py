from flask_login import UserMixin
from sqlalchemy import *

from user import User


class Researcher(User, UserMixin):
    __tablename__ = 'RESEARCHERS'
    userUuid = Column(ForeignKey("USERS.uuid", ondelete='CASCADE'), primary_key=True)
    password = Column(String, nullable=False)
    cv = Column(LargeBinary)

