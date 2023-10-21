from flask_login import UserMixin
from sqlalchemy import *

# classe Admin collegata a nostro DB
class Admin(User, UserMixin):
    __tablename__ = 'ADMIN'
    user_uuid = Column(ForeignKey("USERS.uuid"),primary_key=True) # ondelete='CASCADE'
    password = Column(Text)

    def __init__(self,)
