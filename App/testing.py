import datetime
import enum

from models import *
from sqlalchemy import *
from db import adminSess


from datetime import datetime

def populate_database(session: adminSess):
        # Create an admin user
        admin_user = Admin(name='Admin', surname='User', email='admin@example.com', password='admin_password',
                           dateofbirth=datetime.now())
        adminSess.add(admin_user)

        # Create a researcher user
        researcher_user = Researchers(name='Researcher', surname='User', email='researcher@example.com',
                                      password='researcher_password', dateofbirth=datetime.now(), cv=b'cv_data')
        adminSess.add(researcher_user)

        # Create an evaluator user
        evaluator_user = Evaluator(name='Evaluator', surname='User', email='evaluator@example.com',
                                   password='evaluator_password', dateofbirth=datetime.now(), cv=b'cv_data')
        adminSess.add(evaluator_user)

        # Create a project
        '''project = Project(title='Sample Project', description='This is a sample project', status='approvato')
        adminSess.add(project)'''

        # Create an author association between researcher and project
        '''author_association = Authors(ResearcherUuid=researcher_user.uuid, ProjectUuid=project.uuid)
        adminSess.add(author_association)'''

        # Create a message related to the project
        '''message = Messages(object='Sample Message', text='This is a sample message', date=datetime.now(),
                           ResearcherUuid=researcher_user.uuid, ProjectUuid=project.uuid)
        adminSess.add(message)

        # Create a file related to the project
        file_data = File(title='Sample File', ProjectUuid=project.uuid)
        adminSess.add(file_data)'''

        # Create a version related to the file
        '''version = Versions(details='Version 1', submitdate=datetime.now(), version=1, file=b'version_data',
                           FileUuid=file_data.uuid)
        adminSess.add(version)'''

        # Create a report related to the evaluator and version
        '''report = Report(description='Sample Report', EvaluatorUuid=evaluator_user.userUuid, VersionsUuid=version.uuid)
        adminSess.add(report)'''

        # Commit the changes to the database
        adminSess.commit()

        print("Testing data inserted successfully.")
