from datetime import datetime

import requests
from flask import *
from flask_login import *
from sqlalchemy import *
from App.models import *
from App.db import resSess, adminSess

file_route = Blueprint('file_route', __name__)

@file_route.route('/file_page/<uuid_file>', methods=['GET', 'POST'])
def file_page(uuid_file):
    try:
        if request.method == 'GET':
            # TODO: Aggiungere controllo se l'utente ha accesso a quel file
            file = resSess.execute(select(File).where(File.uuid == uuid_file)).fetchone().File
            print("AAAAA")
            print(file.versions[0].reports)
            return render_template('File.html', file=file)
        elif request.method == 'POST':
            new_prj = Project(title=request.form['title'], description=request.form['description'])
            resSess.add(new_prj)
            resSess.commit()
    except Exception as e:
        print(e)
        resSess.rollback()
    return Response(status=500)
