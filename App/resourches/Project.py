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
        print(f"sono entrato in prj_private {prj_id}")
        if request.method == 'GET':
            prj = resSess.execute(select(Project).where(Project.uuid == prj_id)).fetchone()
            prj = prj.Project
            pro_files = prj.files
            files = [[fl.uuid, fl.title] for fl in pro_files]
            return render_template('Project.html',
                                   files=files,
                                   prj=prj)
        elif request.method == 'POST':
            if request.form.get('action') == "elimina":  # Elimina progetto
                prj_to_remove = request.form['elimina_file']
                resSess.execute(delete(File).where(File.uuid == prj_to_remove))
                resSess.commit()
                return redirect(url_for('prj_route.prj_private', prj_id=prj_id))
    except Exception as e:
        print(e)
        resSess.rollback()
    return Response(status=500)

