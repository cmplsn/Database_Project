from datetime import datetime

from db import Base
from sqlalchemy import *


class Messages(Base):
    __tablename__ = 'MESSAGES'

    uuid = Column(UUID(as_uuid=True), primary_key=True)
    object = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    date = Column(DateTime(timezone=True), default=datetime.now(), nullable=False)
    res = Column(ForeignKey("RESEARCHERS.uuid", ondelete='CASCADE'))
    project = Column(ForeignKey("PROJECT.uuid", ondelete='CASCADE'))

    def __init__(self, object: String, text: Text, date: DateTime, res: UUID, project: UUID, uuid: UUID=null ):
        self.object = object
        self.text = text
        self. date = date
        self.res = res
        self.project = project

        if uuid != null:
            self.uuid = uuid



