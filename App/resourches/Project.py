from datetime import datetime

import requests
from flask import *
from flask_login import *
from sqlalchemy import *
from App.models import *
from App.db import resSess, adminSess

prj_route = Blueprint('prj_route', __name__)


@prj_route.route('/prj_private', methods=['GET', 'POST', 'DELETE', 'PUT'])
def prj_private(prj_id):
    try:
        if request.method == 'GET':
            files = resSess.execute(
                select(File.title).where(
                    File.ProjectUuid == prj_id)).all()
            prj_info = resSess.execute(select(Project.title, Project.description).where(Project.uuid == prj_id)).all()
            return render_template('Project.html',
                                   files=files,
                                   prj=prj_info)
        elif request.method == 'POST':
            if request.form.get('action') == "elimina":  # Elimina progetto
                prj_to_remove = request.form['elimina_file']
                resSess.execute(delete(Project).where(File.uuid == prj_to_remove))
                resSess.commit()
                return redirect(url_for('res_route.res_private'))
            elif request.form.get('action') == "aggiungi":  # Aggiungi progetto
                new_prj = Project(title=request.form['title'], description=request.form['description'])
                resSess.add(new_prj)
                resSess.commit()
    except Exception as e:
        print(e)
        resSess.rollback()
    return redirect(url_for('res_route.res_private'))


@prj_route.route('/file_page/<uuid_file>', methods=['GET', 'POST'])
def file_page(uuid_file):
    #try:
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
    #except Exception as e:
        #print(e)
        #resSess.rollback()
    #return redirect(url_for('res_route.res_private'))
