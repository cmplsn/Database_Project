from datetime import datetime

import requests
from flask import *
from flask_login import *
from sqlalchemy import *
from App.models import *
from App.db import resSess, adminSess

res_route = Blueprint('res_route', __name__)

@login_required
@res_route.route('/res_private', methods=['GET', 'POST', 'DELETE', 'PUT'])
def res_private():
    try:
        if request.method == 'GET':
            column_names = ["Titolo", "Status"]
            open_projects = resSess.execute(
                select(Project.title, Project.status).where(
                    current_user.userUuid == Authors.ResearcherUuid & (
                            Project.uuid == Authors.ProjectUuid) & Project.status is not EvaluationsEnum.approvato)).all()
            approved_projects = resSess.execute(
                select(Project.title).where(
                    current_user.userUuid == Authors.ResearcherUuid & Project.uuid == Authors.ProjectUuid & Project.status is EvaluationsEnum.approvato)).all()
            return render_template('HomeResearcher.html', user=current_user, column_names=column_names,
                                   open_projects=open_projects,
                                   approved_projects=approved_projects)
        elif request.method == 'POST':
            if request.form.get('action') == "elimina":  # Elimina progetto
                prj_to_remove = request.form['elimina_project']
                resSess.execute(delete(Project).where(Project.uuid == prj_to_remove))
                resSess.commit()
                return redirect(url_for('res_route.res_private'))
            elif request.form.get('action') == "aggiungi":  # Aggiungi progetto
                new_prj = Project(title=request.form['title'], description=request.form['description'])
                resSess.add(new_prj)
                resSess.commit()
            elif request.form.get('action') == "submit_to_val":  # submit progetto
                new_prj = Project(title=request.form['title'], description=request.form['description'])
                resSess.add(new_prj)
                resSess.commit()
    except Exception as e:
        print(e)
        resSess.rollback()
    return redirect(url_for('res_route.res_private'))
