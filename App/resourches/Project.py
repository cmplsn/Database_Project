from datetime import datetime

import requests
from flask import *
from flask_login import *
from sqlalchemy import *
from App.models import *
from App.db import resSess, adminSess

prj_route = Blueprint('prj_route', __name__)


@prj_route.route('/prj_private/<prj_id>', methods=['GET', 'POST', 'DELETE', 'PUT'])
def prj_private(prj_id):
    try:
        prj = resSess.execute(select(Project).where(Project.uuid == prj_id)).fetchone()
        prj = prj.Project
        if request.method == 'GET':
            pro_files = prj.files
            pro_messages = prj.messages
            files = [[fl.uuid, fl.title] for fl in pro_files]
            mex = [[mex.text, mex.date, mex.sender] for mex in pro_messages]
            return render_template('Project.html',
                                   files=files,
                                   prj=prj, mex=mex)
        elif request.method == 'POST':
            if request.form.get('action') == "elimina":  # Elimina progetto
                prj_to_remove = request.form['elimina_file']
                resSess.execute(delete(File).where(File.uuid == prj_to_remove))
                resSess.commit()
                return redirect(url_for('prj_route.prj_private', prj_id=prj_id))
            elif request.form.get('action') == "aggiungi":
                file_to_add = request.form['title']
                file = File(title=file_to_add, ProjectUuid=prj.uuid)
                resSess.add(file)
                resSess.commit()
                return redirect(url_for('prj_route.prj_private', prj_id=prj_id))
            elif request.path == f'/prj_private/{prj_id}':
                data = request.get_json()
                mess = Message(sender=data['sender'], text=data['text'], date=data['timestamp'], ProjectUuid=prj.uuid)
                resSess.add(mess)
                resSess.commit()
                return jsonify({'status': 'success'})
    except Exception as e:
        print(e)
        resSess.rollback()
    return Response(status=500)