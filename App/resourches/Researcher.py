from datetime import datetime

import requests
from flask import *
from flask_login import *
from sqlalchemy import *
from provadbmio.App.models import *
from provadbmio.App.db import resSess

res_route = Blueprint('res_route', __name__)


@res_route.route('/res_private', methods=['GET', 'POST', 'DELETE', 'PUT'])
def res_private():
    if request.method == 'GET':
        column_names = ["Name", "Surname", "Email", "Date of Birth", "Remove"]
        data = adminSess.execute(
            select(Users.name, Users.surname, Users.email, Users.dateofbirth, Users.uuid).where(
                Evaluator.userUuid == Users.uuid)).all()
        return render_template('HomeAdmin.html', column_names=column_names, data=data)
    elif request.method == 'POST':
        if request.form.get('action') == "rimuovi":  # Rimuovi Evaluator
            try:
                val_to_remove = request.form['rimuovi_val']
                adminSess.execute(delete(Users).where(Users.uuid == val_to_remove))
                adminSess.commit()
            except Exception as e:
                print(e)
                evSess.rollback()
            return redirect(url_for('admin_route.admin'))
        else:  # Aggiungi Evaluator
            try:
                dateofbirth = datetime.strptime(request.form['dateofbirth'], '%Y-%m-%d')
                new_user = Users(name=request.form['name'], surname=request.form['surname'],
                                 email=request.form['email'], dateofbirth=dateofbirth)
                adminSess.add(new_user)
                adminSess.commit()
                new_eval = Evaluator(userUuid=new_user.uuid, password=request.form['password'], cv=request.form['cv'])
                adminSess.add(new_eval)
                adminSess.commit()
            except Exception as e:
                print(e)
                evSess.rollback()
            return redirect(url_for('admin_route.admin'))
