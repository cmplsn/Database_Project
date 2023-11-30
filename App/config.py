from datetime import datetime
from uuid import UUID

from db import url_admin
from models import EvaluationsEnum, db

class Config:
    # Configurazione del database
    SQLALCHEMY_DATABASE_URI = url_admin
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Dati di esempio per le tabelle
    USERS_DATA = [
        ('Ghost', 'User', 'no.morexisting@ghost.user', datetime(2000, 10, 10)),
        ('Ghost', 'Admin', 'no.morexisting@ghost.admin', datetime(2000, 1, 1)),
        ('Ghost', 'Evaluator', 'no.morexisting@ghost.evaluator', datetime(2000, 2, 2)),
        ('Ghost', 'Researcher', 'no.morexisting@ghost.researcher', datetime(2000, 3, 3)),
    ]

    ADMIN_DATA = [
        ('admin_password',),
    ]

    RESEARCHERS_DATA = [
        ('researcher_password', b'cv_data'),
    ]

    EVALUATOR_DATA = [
        ('evaluator_password', b'cv_data'),
    ]

    PROJECT_DATA = [
        ('Sample Project', 'This is a sample project', EvaluationsEnum.approvato),
    ]

