from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

# url per connessione database admin
url_admin = URL.create('postgresql+psycopg',
                       'admin',
                       'pwd',
                       'localhost',
                       5432,
                       'BasiDiDati')
engine_adm = create_engine(url_admin, echo=True,
                           execution_options={"schema_translate_map": {None: 'project_schema'}})
adminSess = sessionmaker(bind=engine_adm)
adminSess = adminSess()

# url connessione researcher
url_res = URL.create('postgresql+psycopg',
                     'researcher',
                     'pwd',
                     'localhost',
                     5432,
                     'BasiDiDati')
engin_res = create_engine(url_res, echo=True,
                          execution_options={"schema_translate_map": {None: 'project_schema'}})
resSess = sessionmaker(bind=engin_res)
resSess = resSess()

# url connessione evaluator
url_ev = URL.create('postgresql+psycopg',
                    'evaluator',
                    'pwd',
                    'localhost',
                    5432,
                    'BasiDiDati')
engine_ev = create_engine(url_ev, echo=True,
                          execution_options={"schema_translate_map":{None: 'project_schema'}})
evSess = sessionmaker(bind=engine_ev)
evSess = evSess()

