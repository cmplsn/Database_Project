import datetime
from datetime import timedelta

from flask import *
from flask_login import *
from flask_security import Security
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from db import adminSess, resSess, evSess, url_admin
from classes.admin import Admin
from classes.researcher import Researcher
from classes.evaluators import Evaluator
from classes.user import User
from testing import testing


app = Flask(__name__)
app.config['SECRET_KEY'] = 'askh7-wur0z!'
app.config['SQLALCHEMY_DATABASE_URI'] = url_admin
login_manager = LoginManager()
login_manager.init_app(app)

dbase = SQLAlchemy(app)
app.security = Security(app)
# todo: controllare cos'è
# ip_ban = IpBan(ban_count=5)
# ip_ban.init_app(app)

#testing()

print("ho iniziato exe app")


@login_manager.user_loader
def load_user(user_id):
    print('sono entrato in load_user()')
    admin = adminSess.execute(select(Admin).where(Admin.userUuid == user_id)).fetchone()
    if admin is not None:
        print('ho trovato Admin')
        return admin.Admin

    user = evSess.execute(select(User).where(User.uuid==user_id)).fetchone()

    # todo: chiedere elia perchè messo user = teacherSession(...)
    evaluator = evSess.execute(select(Evaluator).where(Evaluator.userUuid == user[0].uuid)).fetchone()
    if evaluator is None:
        researcher = resSess.execute(select(Researcher).where(Researcher.userUuid == user[0].uuid)).fetchone()
        if researcher is not None:
            return researcher.Researcher
    else:
        return evaluator.Evaluator
    print('finita riga 39 codice')

    # aggiungere ritorna errore di caricamento user



@app.route('/')
def home():  # put application's code here
    print('sono entrato in home()')
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    print('sono entrato in login()')
    # settato la chiusura della sessione dopo tempo max 5 minuti
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)

    #riconosco metodo di richiesto come POST dal form html
    if request.method == 'POST':
        try:
            # Verifica se User è presente in db "USER"
            user = evSess.execute(select(User).where(User.email==request.form['email'])).fetchone()
            if user is None:
                return render_template('home.html', login_error=True)

            adm = adminSess.execute(select(Admin).where(Admin.userUuid == user[0].uuid)).fetchone()
            ev = evSess.execute(select(Evaluator).where(Evaluator.userUuid == user[0].uuid)).fetchone()
            res = resSess.execute(select(Researcher).where(Researcher.userUuid == user[0].uuid)).fetchone()

            # Controlla se sta facendo login Admin
            if adm is not None:
                print('ho trovato Admin in login')
                if adm.Admin.auth_pwd(request.form['password']):
                    login_user(adm.Admin)
                    return redirect(url_for('private'))
                else:
                    return render_template('home.html', login_error=True)
            elif ev is not None:
                # Controlla se login è di tipo Evaluator
                ev = ev.Evaluator
                print('ho trovato evaluator in login')
                if ev.auth_pwd(request.form['password']):
                    login_user(ev)
                    return redirect(url_for('private'))
                else:
                    return render_template('home.html', login_error=True)
            elif res is not None:
                # controlla se login è di tipo Researcher
                res = res.Researcher
                print('ho trovato researcher in login')
                if res.auth_pwd(request.form['password']):
                    login_user(res)
                    return redirect(url_for('private'))
                else:
                    return render_template('home.html', login_error=True)
            else:
                return render_template('home.html', login_error=True)
        except Exception as e:
            print(e)
            evSess.rollback()
        return render_template("home.html")
    else:
        if current_user.is_authenticated:
            return redirect(url_for('private'))
        else:
            return render_template('home.html')


@app.route('/private')
@login_required
def private():
    return render_template("private.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()
