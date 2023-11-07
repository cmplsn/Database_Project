import datetime
import enum

from classes.admin import Admin
from classes.user import User
from classes.researcher import Researcher
from classes.evaluators import Evaluator
from classes.authors import authors
from classes.project import Project, EvaluationsEnum
from classes.file import File
from sqlalchemy import *
from db import adminSess


def testing():
    # inserimento Admin,User, Researcher, Evaluator
    adm = Admin('Alessandro','Campagnaro','cmplsn97@gmail.com', 'Abaco123!',
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
                    status=EvaluationsEnum.sottomessoperval.value)

    # Inserimento AUTHOR
    # res.project = [proj1]
    proj1.researchers = [res]
    adminSess.add(res)
    adminSess.add(proj1)

    #Inserimento FILE
    fileprova = File("prova", proj1.uuid)
    adminSess.add(fileprova)
    adminSess.commit()

    """adminSess.execute(delete(User))
    adminSess.execute(delete(Project))
    adminSess.commit()"""
