import enum

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Enum, Date, DateTime, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID


db = SQLAlchemy()


class EvaluationsEnum(enum.Enum):  # todo: capire bene sta cosa degli enum come usarli sia qui che sul DB
    approvato = 1
    sottomessoperval = 2
    modificare = 3
    nonapprovato = 4


class Users(db.Model):
    __tablename__ = 'USERS'

    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=db.text("uuid_generate_v4()"))
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    dateofbirth = Column(Date)


class Admin(db.Model):
    __tablename__ = 'ADMIN'

    userUuid = Column(UUID(as_uuid=True), ForeignKey('USERS.uuid'), primary_key=True)
    password = Column(String, nullable=False)


class Researchers(db.Model):
    __tablename__ = 'RESEARCHERS'

    userUuid = Column(UUID(as_uuid=True), ForeignKey('USERS.uuid'), primary_key=True)
    password = Column(String, nullable=False)
    cv = Column(LargeBinary)


class Evaluator(db.Model):
    __tablename__ = 'EVALUATOR'

    userUuid = Column(UUID(as_uuid=True), ForeignKey('USERS.uuid'), primary_key=True)
    password = Column(String, nullable=False)
    cv = Column(LargeBinary)


class Project(db.Model):
    __tablename__ = 'PROJECT'

    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=db.text("uuid_generate_v4()"))
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(Enum(EvaluationsEnum), nullable=False, default=EvaluationsEnum.modificare)


class Authors(db.Model):
    __tablename__ = 'AUTHORS'

    ResearcherUuid = Column(UUID(as_uuid=True), ForeignKey('RESEARCHERS.userUuid'), primary_key=True)
    ProjectUuid = Column(UUID(as_uuid=True), ForeignKey('PROJECT.uuid'), primary_key=True)

    researcher = relationship('Researchers')
    project = relationship('Project')


class Messages(db.Model):
    __tablename__ = 'MESSAGES'

    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=db.text("uuid_generate_v4()"))
    object = Column(String, nullable=False)
    text = Column(Text)
    date = Column(DateTime)
    ResearcherUuid = Column(UUID(as_uuid=True), ForeignKey('RESEARCHERS.userUuid'), nullable=False)
    ProjectUuid = Column(UUID(as_uuid=True), ForeignKey('PROJECT.uuid'), nullable=False)

    researcher = relationship('Researchers')
    project = relationship('Project')


class File(db.Model):
    __tablename__ = 'FILE'

    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=db.text("uuid_generate_v4()"))
    title = Column(String, nullable=False)
    ProjectUuid = Column(UUID(as_uuid=True), ForeignKey('PROJECT.uuid'), nullable=False)

    project = relationship('Project')
    versions = relationship("Versions", back_populates="file_data")


class Versions(db.Model):
    __tablename__ = 'VERSIONS'

    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=db.text("uuid_generate_v4()"))
    FileUuid = Column(UUID(as_uuid=True), ForeignKey('FILE.uuid', ondelete='CASCADE'))
    details = Column(Text)
    submitdate = Column(DateTime)
    file = Column(LargeBinary)
    version = Column(Integer)

    file_data = relationship('File', back_populates="versions",
                             single_parent=True, cascade='all, delete-orphan')


class Report(db.Model):
    __tablename__ = 'REPORT'

    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=db.text("uuid_generate_v4()"))
    EvaluatorUuid = Column(UUID(as_uuid=True), ForeignKey('EVALUATOR.userUuid'), nullable=False)
    VersionsUuid = Column(UUID(as_uuid=True), ForeignKey('VERSIONS.uuid', ondelete='CASCADE'))
    description = Column(Text)

    evaluator = relationship('Evaluator')
    versions = relationship('Versions')


# Inizializza l'oggetto db con l'app Flask
def init_db(app):
    db.init_app(app)

