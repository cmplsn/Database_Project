from datetime import timedelta, date, datetime
import requests.cookies
from flask import *
from flask_login import *
from flask_login import login_manager
from flask_smorest import *
# from flask_security import Security
# from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from resourches.Project import prj_route
from App.db import *
from App.models import *
from resourches.Admin import admin_route
from resourches.Researcher import res_route
from testing import populate_database

app = Flask(__name__)
app.config['SECRET_KEY'] = 'askh7-wur0z!'
app.config['API_TITLE'] = "BAsi di Dati"
app.config['API_VERSION'] = "v1"
app.config['OPENAPI_VERSION'] = "3.0.3"
app.config['OPENAPI_URL_PREFIX'] = "/"
app.config['OPENAPI_SWAGGER_UI_PATH'] = "/swagger-ui"
app.config['OPENAPI_SWAGGER_UI_URL'] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
# app.config['SQLALCHEMY_DATABASE_URI'] = url_admin
app.register_blueprint(admin_route)
app.register_blueprint(res_route)
app.register_blueprint(prj_route)

login_manager = LoginManager()
login_manager.init_app(app)

api = Api(app)

# dbase = SQLAlchemy(app)
# app.security = Security(app)
# todo: controllare cos'è
# ip_ban = IpBan(ban_count=5)
# ip_ban.init_app(app)


print("ho iniziato exe app")
#populate_database()

@login_manager.user_loader
def load_user(user_id):
    print('sono entrato in load_user()')
    admin = adminSess.execute(select(Admin).where(Admin.userUuid == user_id)).fetchone()
    if admin is not None:
        print('ho trovato Admin')
        return admin.Admin

    user = evSess.execute(select(User).where(User.uuid == user_id)).fetchone()

    # todo: chiedere elia perchè messo user = teacherSession(...)
    evaluator = evSess.execute(select(Evaluator).where(Evaluator.userUuid == user[0].uuid)).fetchone()
    if evaluator is None:
        researcher = resSess.execute(select(Researcher).where(Researcher.userUuid == user[0].uuid)).fetchone()
        if researcher is not None:
            return researcher[0]
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
    #session.permanent = True
    #app.permanent_session_lifetime = timedelta(minutes=5)

    # riconosco metodo di richiesto come POST dal form html
    if request.method == 'POST':
        try:
            # Verifica se User è presente in db "USER"
            user = evSess.execute(select(User).where(User.email == request.form['email'])).fetchone()
            if user is None:
                return render_template('home.html', login_error=True)
            adm = adminSess.execute(select(Admin).where(Admin.userUuid == user[0].uuid)).fetchone()
            print(adm)
            ev = evSess.execute(select(Evaluator).where(Evaluator.userUuid == user[0].uuid)).fetchone()
            res = resSess.execute(select(Researcher).where(Researcher.userUuid == user[0].uuid)).fetchone()

            # Controlla se sta facendo login Admin
            if adm is not None:
                print('ho trovato Admin in login')
                if adm.Admin.auth_pwd(request.form['password']):
                    login_user(adm.Admin)
                    return redirect(url_for('admin_route.admin'))
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
                    return redirect(url_for('res_route.res_private'))
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


def init_database():
    from config import Config
    # Popola il database con i dati di esempio
    with app.app_context():

        for user_data in Config.USERS_DATA:
            users = User(name=user_data[0], surname=user_data[1], email=user_data[2], dateofbirth=user_data[3])
            adminSess.add(users)
        adminSess.commit()

        for admin_data in Config.ADMIN_DATA:
            admin0 = Admin(userUuid=adminSess.execute(select(User).where(User.surname == 'Admin')),
                           password=admin_data[0])
            adminSess.add(admin0)

        for researcher_data in Config.RESEARCHERS_DATA:
            researcher0 = Researcher(userUuid=adminSess.execute(select(User).where(User.surname == 'Researcher')),
                                     cv=researcher_data[2], password=researcher_data[1])
            adminSess.add(researcher0)

        for evaluator_data in Config.EVALUATOR_DATA:
            evaluator0 = Evaluator(userUuid=adminSess.execute(select(User).where(User.surname == 'Evaluator')),
                                   cv=evaluator_data[2], password=evaluator_data[1])
            adminSess.add(evaluator0)

        for project_data in Config.PROJECT_DATA:
            project0 = Project(title=project_data[0], description=project_data[1], status=project_data[2])
            adminSess.add(project0)

        adminSess.commit()


if __name__ == '__main__':
    # init_database()
    #populate_database()
    app.run()
