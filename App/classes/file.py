from sqlalchemy import *
from sqlalchemy.orm import relationship

from db import Base


class File(Base):
    __tablename__ = 'FILE'

    uuid = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(String, nullable=False)
    projectuuid = Column("ProjectUuid", ForeignKey("PROJECT.uuid", ondelete='CASCADE'))
    project = relationship("Project")

    def __init__(self, title: str, projectuuid: UUID, uuid: UUID = null):
        self.projectuuid = projectuuid
        self.title = title

        if uuid != null:
            self.uuid = uuid

    def __repr__(self):
        return f"File(projectuuid:{self.projectuuid}), title='{self.title}', uuid={self.uuid}"

