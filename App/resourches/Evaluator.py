from datetime import datetime
import requests
from flask import *
from flask_login import *
from sqlalchemy import *
from App.models import *
from App.db import resSess, adminSess, evSess

eval_route = Blueprint('eval_route', __name__)


@eval_route.route('/eval_page', methods=['GET', 'POST'])
@login_required
def eval_page():
    try:
        user = evSess.execute(select(Evaluator).where(Evaluator.uuid == current_user.userUuid)).fetchone()
        user = user.Evaluator
        prjts = evSess.execute(select(Project).where(Project.status == EvaluationsEnum.sottomessoperval)).fetchall()
        projects = [[pr.Project.uuid, pr.Project.title] for pr in prjts]
        mex = []
        prj_id = ''
        column_names = ["Titolo", "Vai ai files", "Messaggi", "Aggiorna lo status"]
        if request.method == 'GET':
            return render_template('HomeEvaluator.html', user_name=user.name, column_names=column_names,
                                   projects=projects, mex=mex, prj_id=prj_id)
        elif request.method == 'POST':
            if request.form.get('action') == "vai_ai_files":
                files_to_go = request.form['vai_ai_files']
                return redirect(url_for('eval_files', uuid_project=files_to_go))
            elif request.form.get('action') == "messages":
                id_p = request.form["messages"]
                proj = evSess.execute(select(Project).where(Project.uuid == id_p)).fetchone()
                proj = proj.Project.messages
                mex = [[mex.text, mex.date, mex.sender] for mex in proj]
                return render_template('HomeEvaluator.html', user_name=user.name, column_names=column_names,
                                       projects=projects, mex=mex, prj_id=id_p)
            elif request.path == '/eval_page':
                data = request.get_json()

                mess = Message(sender=not data['sender'], text=data['text'], date=data['timestamp'],
                               ProjectUuid=data['prjid'])
                resSess.add(mess)
                resSess.commit()
                return jsonify({'status': 'success'})
    except Exception as e:
        print(e)
        resSess.rollback()
    return Response(status=500)



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
            newReport = Report(description=request.form['report'], EvaluatorUuid=current_user.userUuid,
                               VersionsUuid=request.form['versionUuid'])
            # TODO: cambiare con ResSess (occhio che non ha i permessi)
            evSess.add(newReport)
            evSess.commit()
            # return redirect(url_for('eval_route.eval_files'))
            return redirect('/eval_files/' + uuid_project)
    except Exception as e:
        print(e)
        resSess.rollback()
        return Response(status=500)
