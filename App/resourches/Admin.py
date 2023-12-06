from datetime import datetime

import requests
from flask import *
from flask_login import *
from sqlalchemy import *
from models import *
from db import adminSess, evSess

admin_route = Blueprint('admin_route', __name__)


@admin_route.route('/admin', methods=['GET', 'POST', 'DELETE', 'PUT'])
def admin():

    if request.method == 'GET':
        column_names = ["Name", "Surname", "Email", "Date of Birth", "Remove"]
        data = adminSess.execute(
            select(User.name, User.surname, User.email, User.birthdate, User.uuid).where(
                Evaluator.userUuid == User.uuid)).all()
        return render_template('HomeAdmin.html', column_names=column_names, data=data)
    elif request.method == 'POST':
        if request.form.get('action') == "rimuovi":  # Rimuovi Evaluator
            try:
                val_to_remove = request.form['rimuovi_val']
                adminSess.execute(delete(User).where(User.uuid == val_to_remove))
                adminSess.commit()
            except Exception as e:
                print(e)
                evSess.rollback()
            return redirect(url_for('admin_route.admin'))
        else:  # Aggiungi Evaluator
            try:
                dateofbirth = datetime.strptime(request.form['dateofbirth'], '%Y-%m-%d')
                new_eval = Evaluator(name=request.form['name'], surname=request.form['surname'],
                                     email=request.form['email'], birthdate=dateofbirth, password=request.form['password'], cv=request.files['cv'].read())
                adminSess.add(new_eval)
                adminSess.commit()
            except Exception as e:
                print(e)
                evSess.rollback()
            return redirect(url_for('admin_route.admin'))
