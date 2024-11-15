from flask import *
from flask_login import *
from sqlalchemy import *
from App.models import *
from App.db import resSess

prj_route = Blueprint('prj_route', __name__)


@prj_route.route('/prj_private/<prj_id>', methods=['GET', 'POST', 'DELETE', 'PUT'])
@login_required
def prj_private(prj_id):  # Pagina dei file di un progetto
    try:
        prj = resSess.execute(select(Project).where(Project.uuid == prj_id)).fetchone()
        prj = prj.Project
        if prj.status == EvaluationsEnum.approvato or prj.status == EvaluationsEnum.nonapprovato:
            closed = True  # closed viene usata per mascherare delle parti del template HTML in base allo status
            # del progetto
        else:
            closed = False
        if request.method == 'GET':
            pro_files = prj.files
            pro_messages = prj.messages
            files = [[fl.uuid, fl.title] for fl in pro_files]
            mex = [[mex.text, mex.date, mex.sender] for mex in pro_messages]
            return render_template('Project.html',
                                   files=files,
                                   prj=prj, mex=mex, closed=closed)
        elif request.method == 'POST':
            if request.form.get('action') == "elimina":
                # Elimina File
                prj_to_remove = request.form['elimina_file']
                resSess.execute(delete(File).where(File.uuid == prj_to_remove))
                resSess.commit()
                return redirect(url_for('prj_route.prj_private', prj_id=prj_id))
            elif request.form.get('action') == "aggiungi":
                # Creazione di un nuovo File
                file_to_add = request.form['title']
                file = File(title=file_to_add, ProjectUuid=prj.uuid)
                resSess.add(file)
                resSess.commit()
                return redirect(url_for('prj_route.prj_private', prj_id=prj_id))
            elif request.path == f'/prj_private/{prj_id}':
                # Handling della messaggistica relativa al progetto
                data = request.get_json()
                mess = Message(sender=data['sender'], text=data['text'], date=data['timestamp'], ProjectUuid=prj.uuid)
                resSess.add(mess)
                resSess.commit()
                return jsonify({'status': 'success'})
    except Exception as e:
        print(e)
        resSess.rollback()
    return Response(status=500)
