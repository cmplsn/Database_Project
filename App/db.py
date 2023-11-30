from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()


# url per connessione database admin
url_admin = URL.create('postgresql+psycopg',
                       'admin_user',
                       'pwd',
                       'localhost',
                       5432,
                       'project_db_database')
engine_adm = create_engine(url_admin, echo=True,
                           execution_options={"schema_translate_map": {None: 'project_schema'}})
adminSess = sessionmaker(bind=engine_adm)
adminSess = adminSess()

# url connessione researcher
url_res = URL.create('postgresql+psycopg',
                     'res_user',
                     'pwd',
                     'localhost',
                     5432,
                     'project_db_database')
engin_res = create_engine(url_res, echo=True,
                          execution_options={"schema_translate_map": {None: 'project_schema'}})
resSess = sessionmaker(bind=engin_res)
resSess = resSess()

# url connessione evaluator
url_ev = URL.create('postgresql+psycopg',
                    'ev_user',
                    'pwd',
                    'localhost',
                    5432,
                    'project_db_database')
engine_ev = create_engine(url_ev, echo=True,
                          execution_options={"schema_translate_map": {None: 'project_schema'}})
evSess = sessionmaker(bind=engine_ev)
evSess = evSess()
