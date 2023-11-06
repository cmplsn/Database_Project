from sqlalchemy.orm import relationship
from db import Base
from sqlalchemy import *
from classes.authors import authors
import enum,uuid


class EvaluationsEnum(enum.Enum):  # todo: capire bene sta cosa degli enum come usarli sia qui che sul DB
    approvato = "approvato"
    sottomessoperval = "sottomesso per valutazione"
    damodificare = "richiede modifiche"
    nonapprovato = "non approvato"


class Project(Base):
    __tablename__ = 'PROJECT'

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(Enum(EvaluationsEnum), nullable=False, default=EvaluationsEnum.sottomessoperval.value)
    researchers = relationship('Researcher', secondary=authors, back_populates="project")
    # file = relationship("File")
    # messages = relationship("Messages")

    def __init__(self, title: str, description: Text, status: EvaluationsEnum, uuid: UUID = null):
        self.title = title
        self.description = description
        self.status = status

        if uuid != null:
            self.uuid = uuid

    # todo: con questa funzione è possibile rappresentare l'istanza come una stringa ben formattata
    def __repr__(self):
        return f"Project(uuid={self.uuid},title={self.title},description={self.description}, status='{self.status}')"

    def EnumToString(self):
        if self.status == EvaluationsEnum.sottomessoperval:
            return 'sottomesso per valutazione'
        elif self.status == EvaluationsEnum.approvato:
            return 'approvato'
        elif self.status == EvaluationsEnum.damodificare:
            return 'richiede modifiche'
        elif self.status == EvaluationsEnum.nonapprovato:
            return 'non approvato'
        else:
            return ''
