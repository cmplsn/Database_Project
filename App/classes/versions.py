import uuid
from datetime import datetime

from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import *


class Versions(Base):
    __tablename__ = 'VERSIONS'

    details = Column(Text)
    submitdate = Column(DateTime(timezone=True), default=datetime.now(), nullable=False)  # todo: cambiare nome sul db
    file = Column(LargeBinary, nullable=False)
    version = Column(Integer, nullable=False)
    fileuuid = Column("FileUuid", ForeignKey("FILE.uuid", ondelete='CASCADE'))
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())

    report = relationship("Report")


    def __init__(self, details: Text, submitdata: DateTime, version: Integer, file: LargeBinary, fileuuid: UUID,
                 uuid: UUID = null):
        self.fileuuid = fileuuid
        self.details = details
        self.submitdata = submitdata
        self.version = version
        self.file = file

        if uuid != null:
            self.uuid = uuid


# todo: serve __repr__ e toJSON???
