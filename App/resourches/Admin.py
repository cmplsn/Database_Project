from datetime import datetime
import requests
from flask import *
from flask_login import *
from sqlalchemy import *
from App.models import *
from App.db import adminSess, evSess

admin_route = Blueprint('admin_route', __name__)


@admin_route.route('/admin', methods=['GET', 'POST', 'DELETE', 'PUT'])
def admin():
    if request.method == 'GET':
        # Riconosco il metodo GET il quale consiste nel selezionare il nome, cognome, email, data di nascita di ogni
        # valutatore e passarli al template HTML per la loro rappresentazione
        column_names = ["Name", "Surname", "Email", "Date of Birth", "Remove"]
        data = adminSess.execute(
            select(User.name, User.surname, User.email, User.birthdate, User.uuid).where(
                Evaluator.userUuid == User.uuid)).all()
        return render_template('HomeAdmin.html', column_names=column_names, data=data)
    elif request.method == 'POST':
        # Il metodo POST ha due azioni principali, l'aggiunta e la rimozione di valutatori
        if request.form.get('action') == "rimuovi":  # Rimuovi valutatore
            try:
                val_to_remove = request.form['rimuovi_val']
                adminSess.execute(delete(User).where(User.uuid == val_to_remove))
                adminSess.commit()
            except Exception as e:
                print(e)
                evSess.rollback()
            return redirect(url_for('admin_route.admin'))
        else:  # Aggiungi valutatore
            try:
                birthdate = datetime.strptime(request.form['birthdate'], '%Y-%m-%d')
                new_eval = Evaluator(name=request.form['name'], surname=request.form['surname'],
                                     email=request.form['email'], birthdate=birthdate, password=request.form['password'], cv=request.files['cv'].read())
                adminSess.add(new_eval)
                adminSess.commit()
            except Exception as e:
                print(e)
                evSess.rollback()
            return redirect(url_for('admin_route.admin'))
