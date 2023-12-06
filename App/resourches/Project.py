from datetime import datetime

import requests
from flask import *
from flask_login import *
from sqlalchemy import *
from App.models import *
from App.db import resSess, adminSess

prj_route = Blueprint('prj_route', __name__)


@prj_route.route('/prj_private', methods=['GET', 'POST', 'DELETE', 'PUT'])
def prj_private():
    try:
        prj_id = 1
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