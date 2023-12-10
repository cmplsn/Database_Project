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
            file = resSess.execute(select(File).where(File.uuid == uuid_file)).fetchone().File
            return render_template('File.html', file=file)
        elif request.method == 'POST':
            resSess.add(Version(submitted=datetime.now(), FileUuid=uuid_file, details=request.form['details'], version=request.form['version'], file=request.files['newVersion'].read()))
            resSess.commit()
            return redirect('/file_page/' + uuid_file)
    except Exception as e:
        print(e)
        resSess.rollback()
        return Response(status=500)


@file_route.route('/get_version/<file_uuid>/<version_uuid>', methods=['GET'])
def get_pdf(file_uuid, version_uuid):
    try:
            # TODO: Aggiungere controllo se l'utente ha accesso a quel file
            ver = resSess.execute(select(Version).where(Version.uuid == version_uuid)).fetchone()
            binary_pdf = ver.Version.file
            response = make_response(binary_pdf)
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = \
                'inline; filename=%s.pdf' % 'yourfilename'
            return response
    except Exception as e:
        print(e)
        resSess.rollback()
        return Response(status=500)
