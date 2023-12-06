import datetime
import enum

from models import *
from sqlalchemy import *
from db import adminSess


from datetime import datetime

def populate_database():
        # Create an admin user
        admin_user = Admin(name='Admin', surname='User', email='adm', password='pwd',
                           birthdate=datetime.now())
        adminSess.add(admin_user)
        adminSess.commit()
        # Create a researcher user
        researcher_user = Researcher(name='Researcher', surname='User', email='res',
                                     password='pwd', birthdate=datetime.now(), cv=b'cv_data')
        adminSess.add(researcher_user)
        adminSess.commit()
        # Create an evaluator user
        evaluator_user = Evaluator(name='Evaluator', surname='User', email='ev',
                                   password='pwd', birthdate=datetime.now(), cv=b'cv_data')
        adminSess.add(evaluator_user)
        adminSess.commit()
        # Create a project
        project = Project(title='Sample Project', description='This is a sample project', status='approvato')
        adminSess.add(project)

        adminSess.commit()

        # Create an author association between researcher and project
        # Create a message related to the project
        message = Message(object='Sample Message', text='This is a sample message', date=datetime.now(),
                          ResearcherUuid=researcher_user.uuid, ProjectUuid=project.uuid)
        adminSess.add(message)
        adminSess.commit()
        # Create a file related to the project
        file_data = File(title='Sample File', ProjectUuid=project.uuid)
        adminSess.add(file_data)
        adminSess.commit()
        # Create a version related to the file
        version = Version(details='Version 1', submitted=datetime.now(), version=1, file=b'version_data',
                          FileUuid=file_data.uuid)
        adminSess.add(version)
        adminSess.commit()
        # Create a report related to the evaluator and version
        report = Report(description='Sample Report', EvaluatorUuid=evaluator_user.userUuid, VersionsUuid=version.uuid)
        adminSess.add(report)

        # Commit the changes to the database
        adminSess.commit()

        print("Testing data inserted successfully.")
