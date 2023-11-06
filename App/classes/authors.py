# Tabella associativa Progetti-Ricercatori
from sqlalchemy import *
from db import Base

authors = Table("AUTHORS", Base.metadata,
                Column('ResearcherUuid', UUID, ForeignKey('RESEARCHERS.userUuid', ondelete='CASCADE'), primary_key=True),
                Column('ProjectUuid', UUID, ForeignKey('PROJECT.uuid', ondelete='CASCADE'), primary_key=True))
