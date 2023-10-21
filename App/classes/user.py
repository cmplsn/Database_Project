from sqlalchemy import *
from db import Base


class User(Base):
    __tablename__ = 'USERS'
    uuid = Column(UUID(as_uuid=True), primary_key=True)  # default=uuid.uuid4)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False)
    dateofbirth = Column('dateofbirth', DateTime, nullable=False)

    def __init__(self, name: str, surname: str, email: str, dateofbirth: DateTime, uuid: UUID = null):
        self.name = name
        self.surname = surname
        self.email = email
        self.dateofbirth = dateofbirth
        if uuid != null:
            self.uuid = uuid

    def __repr__(self):
        return f"User(uuid={self.uuid}, name='{self.name}', surname='{self.surname}', email='{self.email}'," \
                f"dateofbirth = {self.dateofbirth}"

    def get_id(self):
        return self.uuid
