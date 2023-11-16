import datetime
import enum

from classes.admin import Admin
from classes.user import User
from classes.researcher import Researcher
from classes.evaluators import Evaluator
from classes.authors import authors
from classes.project import Project, evaluations_enum
from classes.file import File
from classes.versions import Versions
from classes.messages import Messages
from sqlalchemy import *
from db import adminSess


def testing():
    '''adm = Admin('Alessandro','Campagnaro','cmplsn97@gmail.com', 'Abaco123!',
                   dateofbirth=datetime.date(1997,10,22))
    res = Researcher('Gesù', 'Nazareno', 'gesunazareth@ciao.com', 'PadreFiglio33',
                        cv=open("pdf/CV - Campagnaro Alessandro.pdf",'rb').read(),
                        dateofbirth=datetime.date(1900,12,25))
    ev = Evaluator('Val', 'Utatore', 'val.ut@gmail.com','valuta666',
                      cv=open("pdf/CV - Campagnaro Alessandro.pdf",'rb').read(),
                      dateofbirth=datetime.date(1964,6,14))
    adminSess.add(adm)
    adminSess.add(ev)

    # Inserimento PROJECT

    proj1 = Project("Prova Esempio", "descrizione prova esempio",
                       status=evaluations_enum.sottomessoperval)
    proj2 = Project("PROVA", "descrizione prova esempio2",
                       status=evaluations_enum.nonapprovato)



    # Inserimento AUTHOR
    # res.project = [proj1]
    proj1.researchers = [res]
    adminSess.add(res)
    adminSess.add(proj1)
    adminSess.commit()
    # proj1id = adminSess.execute(select(Project.uuid)).fetchone()

    #Inserimento FILE
    fileprova = File("prova", proj1.uuid)
    adminSess.add(fileprova)
    adminSess.commit()
    vers = Versions("mi sono rotto lo stracazzo", submitdata=datetime.datetime.now(), version=3,
                       file=open("pdf/CV - Campagnaro Alessandro.pdf", 'rb').read(), fileuuid=fileprova.uuid)
    adminSess.add(vers)
    adminSess.commit()'''

    '''rep = Report('descrizione a caso', eval=ev, vers=versi)
    adminSess.add(rep)
    adminSess.commit()'''

    '''adminSess.execute(delete(User))
    adminSess.execute(delete(File))
    adminSess.execute(delete(Project))
    adminSess.commit()'''

    '''res = adminSess.execute(select(Researcher.userUuid)).scalar()
    pro = adminSess.execute(select(Project.uuid)).scalar()
    mex = Messages('messaggio prova', "Buongiorno volevo chiederle se le va bene l'ultima consegna",
                   datetime.datetime.now(), res, pro)
    adminSess.add(mex)
    adminSess.commit()'''

    '''stmt = select(Messages.text).where(Project.messages)
    ret = adminSess.execute(stmt).scalars()
    for row in ret:
        print(row)'''