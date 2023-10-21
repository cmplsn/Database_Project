from flask_login import UserMixin
from sqlalchemy import *
from classes.user import User


# classe Admin collegata a nostro DB
class Admin(User, UserMixin):
    __tablename__ = 'ADMIN'
    userUuid = Column(ForeignKey("USERS.uuid", ondelete='CASCADE'), primary_key=True)
    password = Column(Text, nullable=False)



