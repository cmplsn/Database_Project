from datetime import datetime

import requests
from flask import *
from flask_login import current_user, login_required
from sqlalchemy import *
from models import *
from db import resSess, adminSess

res_route = Blueprint('res_route', __name__)


@res_route.route('/res_private', methods=['GET', 'POST', 'DELETE', 'PUT'])
@login_required
def res_private():
    try:
        user = resSess.execute(select(User).where(User.uuid == current_user.userUuid)).fetchone()
        user = user.User
        email_list = []
        test = resSess.execute(select(Researcher)).fetchone()
        print(test)
        print(test.Researcher.projects)
        if request.method == 'GET':
            column_names = ["Titolo", "Status"]
            open_projects = resSess.execute(
                select(Project.title, Project.status).where(
                    current_user.userUuid == author.ResearcherUuid and (
                            Project.uuid == author.ProjectUuid) and (
                            Project.status is not EvaluationsEnum.approvato))).all()
            approved_projects = resSess.execute(
                select(Project.title).where(
                    current_user.userUuid == author.ResearcherUuid and Project.uuid == Authors.ProjectUuid & Project.status is EvaluationsEnum.approvato)).all()
            return render_template('HomeResearcher.html', user_name=user.name, column_names=column_names,
                                   open_projects=open_projects,
                                   approved_projects=approved_projects, email_array=email_list)
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

                # Crea una relazione tra il nuovo progetto e l'utente corrente
                new_author = author(ResearcherUuid=current_user.uuid, ProjectUuid=new_prj.uuid)
                resSess.add(new_author)

                # Aggiungi gli autori dal form escludendo l'utente corrente
                email_list = request.form.getlist('authors[]')
                for email in email_list:
                    if email != current_user.email:
                        us = resSess.execute(select(User).where(User.email == email)).fetchone()
                        new_author = author(ResearcherUuid=us.uuid, ProjectUuid=new_prj.uuid)
                        resSess.add(new_author)

                resSess.commit()
            elif request.form.get('action') == "submit_to_val":  # submit progetto
                new_prj = Project(title=request.form['title'], description=request.form['description'])
                resSess.add(new_prj)
                resSess.commit()
    except Exception as e:
        print(e)
        resSess.rollback()
        return Response(status=500)  # 500 = codice di errore
    return redirect(url_for('res_route.res_private'))
