from datetime import datetime
import requests
from flask import *
from flask_login import *
from sqlalchemy import *
from App.models import *
from App.db import resSess, adminSess, evSess

eval_route = Blueprint('eval_route', __name__)


@eval_route.route('/eval_files/<uuid_project>', methods=['GET', 'POST'])
def eval_files(uuid_project):
    try:
        if request.method == 'GET':
            project = resSess.execute(select(Project).where(Project.uuid == uuid_project)).fetchone()
            p = project.Project
            asd = resSess.execute(select(Version)).fetchone().Version

            p = project.Project
            for file in p.files:
                prova = file.getLastVersion().Version
                print(prova)
                print(prova.reports)

            return render_template('eval_files.html', project=project.Project)
        elif request.method == 'POST':
            newReport = Report(description=request.form['report'] , EvaluatorUuid=current_user.userUuid, VersionsUuid=request.form['versionUuid'])
            #TODO: cambiare con ResSess (occhio che non ha i permessi)
            evSess.add(newReport)
            evSess.commit()
            #return redirect(url_for('eval_route.eval_files'))
            return redirect('/eval_files/'+uuid_project)
    except Exception as e:
        print(e)
        resSess.rollback()
        return Response(status=500)
