from datetime import datetime

from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import *
import uuid


class Messages(Base):
    __tablename__ = 'MESSAGES'

    uuid = Column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4())
    object = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    date = Column(DateTime(timezone=True), default=datetime.now(), nullable=False)
    researcher = Column('ResearcherUuid', ForeignKey("RESEARCHERS.userUuid", ondelete='CASCADE'))
    project = Column('ProjectUuid', ForeignKey("PROJECT.uuid", ondelete='CASCADE'))
    #res = relationship("Researcher")

    def __init__(self, object: String, text: Text, date: DateTime, researcher: UUID, project: UUID, uuid: UUID=null ):
        self.object = object
        self.text = text
        self. date = date
        self.researcher = researcher
        self.project = project

        if uuid != null:
            self.uuid = uuid



