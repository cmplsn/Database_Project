import datetime

from classes.admin import Admin
from db import adminSess


def testing():
    adm = Admin('A', 'A', 'a@a.com', 'Mika2021!',
                dateofbirth=datetime.date(1997,10,22))
    adminSess.add(adm)
    adminSess.commit()
    adminSess.close()

