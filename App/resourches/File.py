from flask import *
from App.models import *
from App.db import resSess

file_route = Blueprint('file_route', __name__)


@file_route.route('/file_page/<uuid_file>', methods=['GET', 'POST'])
def file_page(uuid_file):  # Pagina delle versioni di un progetto
    try:
        if request.method == 'GET':
            # raccolta dei file di un progetto
            file = resSess.execute(select(File).where(File.uuid == uuid_file)).fetchone().File
            prj = resSess.execute(select(Project).where(Project.uuid == file.ProjectUuid)).fetchone()
            prj = prj.Project
            if prj.status == EvaluationsEnum.approvato or prj.status == EvaluationsEnum.nonapprovato:
                closed = True  # closed viene usata per mascherare delle parti del template HTML in base allo status
                # del progetto
            else:
                closed = False
            return render_template('File.html', file=file, closed=closed)
        elif request.method == 'POST':
            # Creazione di una nuova versione
            resSess.add(Version(submitted=datetime.now(), FileUuid=uuid_file, details=request.form['details'],
                                version=request.form['version'], file=request.files['newVersion'].read()))
            resSess.commit()
            return redirect('/file_page/' + uuid_file)
    except Exception as e:
        print(e)
        resSess.rollback()
        return Response(status=500)


@file_route.route('/get_version/<file_uuid>/<version_uuid>', methods=['GET'])
def get_pdf(file_uuid, version_uuid):
    try:
        # Visualizzazione della versione (file PDF)
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
