import bcrypt
from flask_login import UserMixin
from sqlalchemy import *
from sqlalchemy.orm import relationship
from user import User


class Evaluator(User, UserMixin):
    __tablename__ = 'EVALUATORS'

    userUuid = Column(ForeignKey("USERS.uuid", ondelete='CASCADE'), primary_key=True)
    password = Column(String, nullable=False)
    cv = Column(LargeBinary)

