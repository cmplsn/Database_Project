import datetime
import enum
from datetime import datetime

import bcrypt
import uuid

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Enum, Date, DateTime, LargeBinary, null, Table, desc, \
    select, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from App.db import Base, resSess


db = SQLAlchemy()


class EvaluationsEnum(enum.Enum):  # todo: capire bene sta cosa degli enum come usarli sia qui che sul DB
    approvato = 1
    sottomessoperval = 2
    modificare = 3
    nonapprovato = 4

    @staticmethod
    def getStringEvaluation(enum):
        if enum == EvaluationsEnum.approvato: return 'APPROVATO'
        elif enum == EvaluationsEnum.sottomessoperval: return 'SOTTOMESSO PER VALUTAZIONE'
        elif enum == EvaluationsEnum.modificare: return 'MODIFICARE'
        else: return 'NON APPROVATO'

    @staticmethod
    def getEvaluationsEnum(str):
        if str == 'APPROVATO': return EvaluationsEnum.approvato
        elif str == 'SOTTOMESSO PER VALUTAZIONE': return EvaluationsEnum.sottomessoperval
        elif str == 'MODIFICARE': return EvaluationsEnum.modificare
        else: return EvaluationsEnum.nonapprovato


class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    birthdate = Column(Date)

    def __init__(self, name: str, surname: str, email: str, dateofbirth: DateTime, uuid: UUID = null):
        self.name = name
        self.surname = surname
        self.email = email
        self.birthdate = dateofbirth
        if uuid != null:
            self.uuid = uuid

    def __repr__(self):
        return f"User(uuid={self.uuid}, name='{self.name}', surname='{self.surname}', email='{self.email}'," \
               f"birthdate = {self.birthdate}"

    def get_id(self):
        return self.uuid


class Admin(User, UserMixin):
    __tablename__ = 'admin'
    __table_args__ = {'extend_existing': True}
    userUuid = Column('userUuid', ForeignKey('users.uuid', ondelete='CASCADE'), primary_key=True)
    password = Column(String, nullable=False)

    def __init__(self, name: str, surname: str, email: str, password: str, birthdate: DateTime, uuid: UUID = null):
        super().__init__(name, surname, email, birthdate, uuid)
        pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.password = pwd.decode('utf-8')
        self.userUuid = self.uuid

    def auth_pwd(self, pwd: str):
        return bcrypt.checkpw(pwd.encode('utf-8'), self.password.encode('utf-8'))

    def toJSON(self):
        return {'uuid': str(super().uuid),
                'name': super().name,
                'surname': super().surname,
                'email': super().email,
                'birthdate': str(super().birthdate)}

    def __repr__(self):
        return (f"Admin(userUuid:{self.userUuid},name = '{self.name}', surname='{self.surname}',"
                f"email:{self.email}, password='***', birthdate={self.birthdate},uuid={self.uuid})")


author = db.Table(
    'authors',
    db.Column('ProjectUuid', UUID(as_uuid=True), db.ForeignKey('projects.uuid'), primary_key=True),
    db.Column('ResearcherUuid', UUID(as_uuid=True), db.ForeignKey('researchers.userUuid'), primary_key=True),
    extend_existing=True
)


class Researcher(User, UserMixin):
    __tablename__ = 'researchers'
    __table_args__ = {'extend_existing': True}
    userUuid = Column('userUuid', ForeignKey('users.uuid', ondelete='CASCADE'), primary_key=True)
    password = Column(String, nullable=False)
    cv = Column(LargeBinary)
    projects = relationship("Project", secondary=author, backref='researcher')

    def __init__(self, name: str, surname: str, email: str, password: str, birthdate: DateTime, cv: LargeBinary,
                 uuid: UUID = null):
        super().__init__(name, surname, email, birthdate, uuid)
        pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.password = pwd.decode('utf-8')
        self.cv = cv
        self.userUuid = self.uuid

    def auth_pwd(self, pwd: str):
        return bcrypt.checkpw(pwd.encode('utf-8'), self.password.encode('utf-8'))


class Project(db.Model):
    __tablename__ = 'projects'
    __table_args__ = {'extend_existing': True}
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(Enum(EvaluationsEnum), nullable=False, default=EvaluationsEnum.sottomessoperval)
    researchers = relationship("Researcher", secondary=author, backref='project')
    files = relationship("File", back_populates="project")
    messages = relationship("Message", back_populates="project")

class Evaluator(User, UserMixin):
    __tablename__ = 'evaluators'
    __table_args__ = {'extend_existing': True}
    userUuid = Column('userUuid', ForeignKey('users.uuid', ondelete='CASCADE'), primary_key=True)
    password = Column(String, nullable=False)
    cv = Column(LargeBinary)

    def __init__(self, name: str, surname: str, email: str, password: str, birthdate: DateTime, cv: LargeBinary,
                 uuid: UUID = null):
        super().__init__(name, surname, email, birthdate, uuid)
        pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.cv = cv
        self.password = pwd.decode('utf-8')
        self.userUuid = self.uuid

    def auth_pwd(self, pwd: str):
        return bcrypt.checkpw(pwd.encode('utf-8'), self.password.encode('utf-8'))


class Message(db.Model):
    __tablename__ = 'messages'
    __table_args__ = {'extend_existing': True}
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sender = Column(Boolean, nullable=False)
    text = Column(Text)
    date = Column(DateTime)
    ProjectUuid = Column(UUID(as_uuid=True), ForeignKey('projects.uuid'), nullable=False)
    project = relationship("Project", back_populates="messages")
    def __init__(self, sender: bool, text: Text, date: DateTime, ProjectUuid: UUID,
                 uuid: UUID = null):
        self.sender = sender
        self.text = text
        self.date = date
        self.ProjectUuid = ProjectUuid

        if uuid != null:
            self.uuid = uuid


class File(db.Model):
    __tablename__ = 'files'
    __table_args__ = {'extend_existing': True}
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    ProjectUuid = Column(UUID(as_uuid=True), ForeignKey('projects.uuid'), nullable=False)
    versions = relationship("Version", back_populates="files")
    project = relationship("Project", back_populates="files")

    def __init__(self, title: str, ProjectUuid: UUID, uuid: UUID = null):
        self.ProjectUuid = ProjectUuid
        self.title = title

        if uuid != null:
            self.uuid = uuid

    def getLastVersion(self):
        last_version = resSess.execute(select(Version).filter_by(FileUuid=self.uuid).order_by(desc(Version.submitted))).first()
        return last_version

    def __repr__(self):
        return f"File(projectuuid:{self.projectuuid}), title='{self.title}', uuid={self.uuid}"


class Version(db.Model):
    __tablename__ = 'versions'
    __table_args__ = {'extend_existing': True}
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    FileUuid = Column(UUID(as_uuid=True), ForeignKey('files.uuid', ondelete='CASCADE'))
    details = Column(Text)
    submitted = Column(DateTime, default=datetime.now())
    file = Column(LargeBinary)
    version = Column(Integer, nullable=False)
    files = relationship("File", back_populates="versions")

    reports = relationship("Report", back_populates="version")
    def getLastReport(self):
        last_report = resSess.execute(select(Report).filter_by(VersionsUuid=self.uuid).order_by(desc(Report.submitted))).first()
        return last_report

    def __repr__(self):
        return f"<Version(uuid='{self.uuid}', FileUuid='{self.FileUuid}', details='{self.details}', submitted='{self.submitted}', version='{self.version}')>"

    def __init__(self, details: Text, submitted: DateTime, version: Integer, file: LargeBinary, FileUuid: UUID,
                 uuid: UUID = null):
        self.FileUuid = FileUuid
        self.details = details
        self.submitted = submitted
        self.version = version
        self.file = file

        if uuid != null:
            self.uuid = uuid

    def __str__(self):
        return (f"Version ID: {self.uuid}, File ID: {self.FileUuid}, Details: {self.details}, "
                f"Submitted: {self.submitted}, Version: {self.version}")


class Report(db.Model):
    __tablename__ = 'reports'
    __table_args__ = {'extend_existing': True}
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    EvaluatorUuid = Column(UUID(as_uuid=True), ForeignKey('evaluators.userUuid'), nullable=False)
    VersionsUuid = Column(UUID(as_uuid=True), ForeignKey('versions.uuid', ondelete='CASCADE'))
    description = Column(Text)
    file = Column(LargeBinary)
    submitted = Column(DateTime, default=datetime.now())
    version = relationship("Version", back_populates="reports")

    def __init__(self, description: Text, EvaluatorUuid: UUID, VersionsUuid: UUID, file: LargeBinary, uuid: UUID = null):
        self.description = description
        self.EvaluatorUuid = EvaluatorUuid
        self.file = file
        self.VersionsUuid = VersionsUuid

        if uuid != null:
            self.uuid = uuid


# Inizializza l'oggetto db con l'app Flask
def init_db(app):
    db.init_app(app)
    with app.app_context():
        Base.metadata.create_all()
