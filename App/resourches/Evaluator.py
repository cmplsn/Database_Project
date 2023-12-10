from flask import *
from flask_login import *
from App.models import *
from App.db import evSess

eval_route = Blueprint('eval_route', __name__)


@eval_route.route('/eval_page', methods=['GET', 'POST'])
@login_required
def eval_page():  # Pagina principale dell'area riservata del valutatore
    try:
        # Reperimento dei dati da inviare al template HTML
        user = evSess.execute(select(Evaluator).where(Evaluator.uuid == current_user.userUuid)).fetchone()
        user = user.Evaluator
        prjts = evSess.execute(select(Project).where(Project.status == EvaluationsEnum.sottomessoperval)).fetchall()
        projects = [[pr.Project.uuid, pr.Project.title] for pr in prjts]
        mex = []
        prj_id = ''
        column_names = ["Titolo", "Messaggi", "Aggiorna lo status"]
        if request.method == 'GET':
            return render_template('HomeEvaluator.html', user_name=user.name, column_names=column_names,
                                   projects=projects, mex=mex, prj_id=prj_id)
        elif request.method == 'POST':
            if request.form.get('action') == "messages":
                # è stato premuto il button messages per visualizzare i messaggi relativi a un determinato progetto,
                # questa parte del codice raccoglie tutti i messaggi e li invia al template HTML
                id_p = request.form["messages"]
                proj = evSess.execute(select(Project).where(Project.uuid == id_p)).fetchone()
                proj = proj.Project.messages
                mex = [[mex.text, mex.date, not mex.sender] for mex in proj]
                return render_template('HomeEvaluator.html', user_name=user.name, column_names=column_names,
                                       projects=projects, mex=mex, prj_id=id_p)
            elif request.form.get('action') == "status":
                # è stato scelto uno status da assegnare a un determinato progetto, questa sezione di codice si
                # occupa dell'upgrade dello status di quel determinato progetto
                status = EvaluationsEnum.getEvaluationsEnum(request.form['status'])
                id_p = request.form['id_prg']
                proj = evSess.execute(select(Project).where(Project.uuid == id_p)).fetchone()
                proj.Project.status = status
                evSess.commit()
                return redirect('/eval_page')
            elif request.path == '/eval_page':
                # Invio di un messaggio
                data = request.get_json()
                prj_uuid = data['projectId']
                mess = Message(sender=not data['sender'], text=data['text'], date=data['timestamp'],
                               ProjectUuid=prj_uuid)
                evSess.add(mess)
                evSess.commit()
                return jsonify({'status': 'success'})
    except Exception as e:
        print(e)
        evSess.rollback()
    return Response(status=500)


@eval_route.route('/eval_files/<uuid_project>', methods=['GET', 'POST'])
@login_required
def eval_files(uuid_project):  # Visualizzazione dei file di un progetto
    try:
        if request.method == 'GET':
            # Per ogni file viene mostrata l'ultima versione in ordine cronologico di creazione
            project = evSess.execute(select(Project).where(Project.uuid == uuid_project)).fetchone()
            p = project.Project
            asd = evSess.execute(select(Version)).fetchone().Version

            p = project.Project
            for file in p.files:
                prova = file.getLastVersion().Version

            return render_template('eval_files.html', project=project.Project)
        elif request.method == 'POST':
            newReport = Report(description=request.form['report'], EvaluatorUuid=current_user.userUuid,
                               VersionsUuid=request.form['versionUuid'], file=request.files['newreport'].read())
            evSess.add(newReport)
            evSess.commit()
            return redirect('/eval_files/' + uuid_project)
    except Exception as e:
        print(e)
        evSess.rollback()
        return Response(status=500)


@eval_route.route('/get_report/<file_uuid>/<report_uuid>', methods=['GET'])
@login_required
def get_pdf(file_uuid, report_uuid):
    try:
        # Visualizzazione del file PDF
        rep = evSess.execute(select(Report).where(Report.uuid == report_uuid)).fetchone()
        binary_pdf = rep.Report.file
        response = make_response(binary_pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = \
            'inline; filename=%s.pdf' % 'yourfilename'
        return response
    except Exception as e:
        print(e)
        evSess.rollback()
        return Response(status=500)
