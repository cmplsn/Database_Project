import datetime
import enum

from models import *
from sqlalchemy import *
from db import adminSess


from datetime import datetime

def populate_database(session: adminSess):
    # Inserisci un utente
    user0 = Users(name='Ghost', surname='User', email='no.morexisting@ghost.user', dateofbirth=datetime(2000, 10, 10))
    user1 = Admin(name='Ghost', surname='Admin', email='no.morexisting@ghost.admin', dateofbirth=datetime(2000, 1, 1), password='admin_password')
    user2 = Evaluator(name='Ghost', surname='Evaluator', email='no.morexisting@ghost.evaluator', dateofbirth=datetime(2000, 2, 2), password='evaluator_password', cv=b'cv_data')
    user3 = Researchers(name='Ghost', surname='Researcher', email='no.morexisting@ghost.researcher', dateofbirth=datetime(2000, 3, 3), cv=b'cv_data', password='researcher_password')
    session.add(user0)
    session.commit()
    session.add(user1)
    session.add(user2)
    session.add(user3)
    session.commit()

    # Inserisci un progetto
    project = Project(title='Sample Project', description='This is a sample project', status='approvato')
    session.add(project)
    session.commit()

    # Inserisci un messaggio
    '''message = Messages(object='Sample Message', text='This is a sample message', date=datetime.now(),
                       ResearcherUuid=researcher.userUuid, ProjectUuid=project.uuid)
    session.add(message)
    session.commit()

    # Inserisci un file
    file = File(title='Sample File', ProjectUuid=project.uuid)
    session.add(file)
    session.commit()

    # Inserisci una versione
    version = Versions(FileUuid=file.uuid, details='Sample Version', submitdate=datetime.now(), file=b'version_data', version=1)
    session.add(version)
    session.commit()

    # Inserisci un report
    report = Report(EvaluatorUuid=evaluator.userUuid, VersionsUuid=version.uuid, description='Sample Report')
    session.add(report)
    session.commit()

    # Inserisci una relazione autore
    author_relation = Authors(ResearcherUuid=researcher.userUuid, ProjectUuid=project.uuid)
    session.add(author_relation)
    session.commit()

# Esempio di utilizzo
# from your_flask_app import db, app
# with app.app_context():
#     db.create_all()
#     populate_database(db.session)'''
