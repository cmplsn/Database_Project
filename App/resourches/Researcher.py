from flask import *
from flask_login import current_user, login_required
from sqlalchemy import *
from App.models import *
from App.db import resSess

res_route = Blueprint('res_route', __name__)


@res_route.route('/res_private', methods=['GET', 'POST', 'DELETE', 'PUT'])
@login_required
def res_private():  # Pagina principale dell'area riservata del ricercatore
    try:
        user = resSess.execute(select(Researcher).where(Researcher.uuid == current_user.userUuid)).fetchone()
        user = user.Researcher
        email_list = []
        test = user.projects
        if request.method == 'GET':
            # Visualizzazione dei progetti modificabili (con status = modificare / sottomesso per valutazione) e non
            # (con status = approvato / rifiutato)
            column_names = ["Titolo", "Status"]
            open_projects = [[prj.uuid, prj.title, EvaluationsEnum.getStringEvaluation(prj.status)] for prj in test if
                             prj.status != EvaluationsEnum.approvato]
            closed_projects = [[prj.uuid, prj.title, EvaluationsEnum.getStringEvaluation(prj.status)] for prj in test if
                                 prj.status == EvaluationsEnum.approvato or prj.status == EvaluationsEnum.nonapprovato]
            return render_template('HomeResearcher.html', user_name=user.name, column_names=column_names,
                                   open_projects=open_projects,
                                   closed_projects=closed_projects, email_array=email_list)
        elif request.method == 'POST':
            if request.form.get('action') == "elimina":
                # Elimina progetto
                prj_to_remove = request.form['elimina_project']
                resSess.execute(delete(Project).where(Project.uuid == prj_to_remove))
                resSess.commit()
                return redirect(url_for('res_route.res_private'))
            elif request.form.get('action') == "submit_to_val":
                # Aggiornamento dello status del progetto a sottomesso per valutazione
                prj_to_update = request.form['submit_to_val']
                prj = resSess.execute(select(Project).where(Project.uuid == prj_to_update)).fetchone()
                prj = prj.Project
                prj.status = EvaluationsEnum.sottomessoperval
                resSess.commit()
                return redirect(url_for('res_route.res_private'))
            elif request.path == '/res_private':
                # Aggiungi progetto
                data = request.get_json()
                new_prj = Project(title=data['title'], description=data['description'])
                # Aggiunta degli autori dal form escludendo l'utente corrente
                for email in data['emails']:
                    if email != current_user.email:
                        us = resSess.execute(select(Researcher).where(Researcher.email == email)).fetchone()
                        if us:
                            us = us.Researcher
                            new_prj.researchers.append(us)
                # Aggiunta dell'utente corrente
                new_prj.researchers.append(user)
                resSess.add(new_prj)
                resSess.commit()
                return jsonify({'status': 'success'})
            elif request.form.get('action') == "redirect":  # Redirect progetto
                prj_id_to_redirect = request.form['prj_id']
                return redirect(url_for('prj_route.prj_private', prj_id=prj_id_to_redirect))
    except Exception as e:
        print(e)
        resSess.rollback()
        return Response(status=500)  # 500 = codice di errore