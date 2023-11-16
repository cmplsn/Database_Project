from sqlalchemy.orm import relationship
from db import Base
from sqlalchemy import *
from classes.authors import authors
import enum
import uuid
from classes.messages import Messages
from classes.file import File


class evaluations_enum(enum.Enum):  # todo: capire bene sta cosa degli enum come usarli sia qui che sul DB
    approvato = 1
    sottomessoperval = 2
    modificare = 3
    nonapprovato = 4


class Project(Base):
    __tablename__ = 'PROJECT'

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(Enum(evaluations_enum), nullable=False, default=evaluations_enum.sottomessoperval.name)
    researchers = relationship('Researcher', secondary=authors, back_populates="project")
    files = relationship(File, backref="Project")
    messages = relationship(Messages)

    def __init__(self, title: str, description: Text, status: evaluations_enum, uuid: UUID = null):
        self.title = title
        self.description = description
        self.status = status

        if uuid != null:
            self.uuid = uuid

    # todo: con questa funzione è possibile rappresentare l'istanza come una stringa ben formattata
    def __repr__(self):
        return f"Project(uuid={self.uuid},title='{self.title}',description={self.description},"\
               f"status='{self.status}')"

    def EnumToString(self):
        if self.status == evaluations_enum.sottomessoperval:
            return 'sottomesso per valutazione'
        elif self.status == evaluations_enum.approvato:
            return 'approvato'
        elif self.status == evaluations_enum.damodificare:
            return 'richiede modifiche'
        elif self.status == evaluations_enum.nonapprovato:
            return 'non approvato'
        else:
            return ''
