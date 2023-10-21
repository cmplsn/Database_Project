from sqlalchemy.orm import relationship
from db import Base
from sqlalchemy import *
from classes.authors import authors
import enum


class EvaluationsEnum(enum.Enum): # todo: capire bene sta cosa degli enum come usarli sia qui che sul DB
    approvato = 1
    sottomessoperval = 2
    damodificare = 3
    nonapprovato = 4


class Project(Base):
    __tablename__ = 'PROJECT'
    uuid = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(Enum(EvaluationsEnum), nullable=False)
    authors = relationship("Researcher", secondary=authors, back_populates="PROJECT")
    file = relationship("File")
    messages = relationship("Messages")

    def __init__(self, title: str, description: Text, status: EvaluationsEnum, uuid: UUID = null):
        self.title = title
        self.description = description
        self.status = status

        if uuid != null:
            self.uuid = uuid

    # todo: con questa funzione è possibile rappresentare l'istanza come una stringa ben formattata
    # def __repr__(self):
        # return f"Project(uuid={self.uuid},title={self.title},description={self.description}, status='{self.status}')"