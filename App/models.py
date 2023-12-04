import enum

import bcrypt
import uuid

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Enum, Date, DateTime, LargeBinary, null
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from db import Base

db = SQLAlchemy()

class EvaluationsEnum(enum.Enum):  # todo: capire bene sta cosa degli enum come usarli sia qui che sul DB
    approvato = 1
    sottomessoperval = 2
    modificare = 3
    nonapprovato = 4


class Users(Base):
    __tablename__ = 'USERS'
    __table_args__ = {'extend_existing': True}
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    dateofbirth = Column(Date)

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


class Admin(Users, UserMixin):
    __tablename__ = 'ADMIN'
    __table_args__ = {'extend_existing': True}
    userUuid = Column('userUuid', ForeignKey('USERS.uuid', ondelete='CASCADE'), primary_key=True)
    password = Column(String, nullable=False)

    def __init__(self, name: str, surname: str, email: str, password: str, dateofbirth: DateTime, uuid: UUID = null):
        super().__init__(name, surname, email, dateofbirth, uuid)
        pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.password = pwd.decode('utf-8')

    def auth_pwd(self, pwd: str):
        return bcrypt.checkpw(pwd.encode('utf-8'), self.password.encode('utf-8'))

    def toJSON(self):
        return {'uuid': str(super().uuid),
                'name': super().name,
                'surname': super().surname,
                'email': super().email,
                'dateofbirth': str(super().dateofbirth)}

    def __repr__(self):
        return (f"Admin(userUuid:{self.userUuid},name = '{self.name}', surname='{self.surname}',"
                f"email:{self.email}, password='***', dateofbirt={self.dateofbirth},uuid={self.uuid})")


class Researchers(Users, UserMixin):
    __tablename__ = 'RESEARCHERS'
    __table_args__ = {'extend_existing': True}
    userUuid = Column('userUuid', ForeignKey('USERS.uuid', ondelete='CASCADE'), primary_key=True)
    password = Column(String, nullable=False)
    cv = Column(LargeBinary)

    def __init__(self, name: str, surname: str, email: str, password: str, dateofbirth: DateTime, cv: LargeBinary, uuid: UUID = null):
        super().__init__(name, surname, email, dateofbirth, uuid)
        pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.password = pwd.decode('utf-8')
        self.cv = cv


class Evaluator(Users, UserMixin):
    __tablename__ = 'EVALUATOR'
    __table_args__ = {'extend_existing': True}
    userUuid = Column('userUuid', ForeignKey('USERS.uuid', ondelete='CASCADE'), primary_key=True)
    password = Column(String, nullable=False)
    cv = Column(LargeBinary)

    def __init__(self, name: str, surname: str, email: str, password: str, dateofbirth: DateTime, cv: LargeBinary,
                 uuid: UUID = null):
        super().__init__(name, surname, email, dateofbirth, uuid)
        pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.cv = cv
        self.password = pwd.decode('utf-8')


class Project(db.Model):
    __tablename__ = 'PROJECT'
    __table_args__ = {'extend_existing': True}
    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=db.text("uuid_generate_v4()"))
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(Enum(EvaluationsEnum), nullable=False, default=EvaluationsEnum.modificare)


class Authors(db.Model):
    __tablename__ = 'AUTHORS'
    __table_args__ = {'extend_existing': True}
    ResearcherUuid = Column(UUID(as_uuid=True), ForeignKey('RESEARCHERS.userUuid'), primary_key=True)
    ProjectUuid = Column(UUID(as_uuid=True), ForeignKey('PROJECT.uuid'), primary_key=True)

    researcher = relationship('Researchers')
    project = relationship('Project')


class Messages(db.Model):
    __tablename__ = 'MESSAGES'
    __table_args__ = {'extend_existing': True}
    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=db.text("uuid_generate_v4()"))
    object = Column(String, nullable=False)
    text = Column(Text)
    date = Column(DateTime)
    ResearcherUuid = Column(UUID(as_uuid=True), ForeignKey('RESEARCHERS.userUuid'), nullable=False)
    ProjectUuid = Column(UUID(as_uuid=True), ForeignKey('PROJECT.uuid'), nullable=False)

    researcher = relationship('Researchers')
    project = relationship('Project')

    def __init__(self, object: String, text: Text, date: DateTime, res: UUID, project: UUID, uuid: UUID = null):
        self.object = object
        self.text = text
        self.date = date
        self.res = res
        self.project = project

        if uuid != null:
            self.uuid = uuid


class File(db.Model):
    __tablename__ = 'FILE'
    __table_args__ = {'extend_existing': True}
    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=db.text("uuid_generate_v4()"))
    title = Column(String, nullable=False)
    ProjectUuid = Column(UUID(as_uuid=True), ForeignKey('PROJECT.uuid'), nullable=False)

    project = relationship('Project')
    versions = relationship("Versions", back_populates="file_data")

    def __init__(self, title: str, projectuuid: UUID, uuid: UUID = null):
        self.projectuuid = projectuuid
        self.title = title

        if uuid != null:
            self.uuid = uuid

    def __repr__(self):
        return f"File(projectuuid:{self.projectuuid}), title='{self.title}', uuid={self.uuid}"


class Versions(db.Model):
    __tablename__ = 'VERSIONS'
    __table_args__ = {'extend_existing': True}
    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=db.text("uuid_generate_v4()"))
    FileUuid = Column(UUID(as_uuid=True), ForeignKey('FILE.uuid', ondelete='CASCADE'))
    details = Column(Text)
    submitdate = Column(DateTime)
    file = Column(LargeBinary)
    version = Column(Integer)

    file_data = relationship('File', back_populates="versions",
                             single_parent=True, cascade='all, delete-orphan')

    def __init__(self, details: Text, submitdata: DateTime, version: Integer, file: LargeBinary, fileuuid: UUID,
                 uuid: UUID = null):
        self.fileuuid = fileuuid
        self.details = details
        self.submitdata = submitdata
        self.version = version
        self.file = file

        if uuid != null:
            self.uuid = uuid


class Report(db.Model):
    __tablename__ = 'REPORT'
    __table_args__ = {'extend_existing': True}
    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=db.text("uuid_generate_v4()"))
    EvaluatorUuid = Column(UUID(as_uuid=True), ForeignKey('EVALUATOR.userUuid'), nullable=False)
    VersionsUuid = Column(UUID(as_uuid=True), ForeignKey('VERSIONS.uuid', ondelete='CASCADE'))
    description = Column(Text)

    evaluator = relationship('Evaluator')
    versions = relationship('Versions')

    def __init__(self, description: Text, eval: UUID, vers: UUID, uuid: UUID = null):
        self.description = description
        self.eval = eval
        self.vers = vers

        if uuid != null:
            self.uuid = uuid


# Inizializza l'oggetto db con l'app Flask
def init_db(app):
    db.init_app(app)
    with app.app_context():
        Base.metadata.create_all()
