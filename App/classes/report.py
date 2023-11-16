from db import Base
from sqlalchemy import *
import uuid


class Report(Base):
    __tablename__ = 'REPORT'
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description = Column(Text, nullable=False)
    eval = Column(ForeignKey("EVALUATOR.userUuid", ondelete='CASCADE'))
    vers = Column(ForeignKey("VERSIONS.uuid", ondelete='CASCADE'))

    def __init__(self, description: Text, eval: UUID, vers: UUID, uuid: UUID = null):
        self.description = description
        self.eval = eval
        self.vers = vers

        if uuid != null:
            self.uuid = uuid


