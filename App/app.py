from flask import *
from flask_ipban import IpBan
from flask_login import *
from resourches.Evaluator import eval_route
from resourches.File import file_route
from resourches.Project import prj_route
from App.db import *
from models import *
from resourches.Admin import admin_route
from resourches.Researcher import res_route
from testing import populate_database

app = Flask(__name__)
app.config['SECRET_KEY'] = 'askh7-wur0z!'
app.config['API_TITLE'] = "Basi di Dati"

app.register_blueprint(admin_route)
app.register_blueprint(res_route)
app.register_blueprint(prj_route)
app.register_blueprint(eval_route)
app.register_blueprint(file_route)

login_manager = LoginManager()
login_manager.init_app(app)

ip_ban = IpBan(ban_count=5)
ip_ban.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    print('sono entrato in load_user()')
    admin = adminSess.execute(select(Admin).where(Admin.userUuid == user_id)).fetchone()
    if admin is not None:
        print('ho trovato Admin')
        return admin.Admin
    user = evSess.execute(select(User).where(User.uuid == user_id)).fetchone()
    evaluator = evSess.execute(select(Evaluator).where(Evaluator.userUuid == user[0].uuid)).fetchone()
    if evaluator is None:
        researcher = resSess.execute(select(Researcher).where(Researcher.userUuid == user[0].uuid)).fetchone()
        if researcher is not None:
            return researcher[0]
    else:
        return evaluator.Evaluator


@app.route('/')
def home():
    return redirect(url_for('registration'))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    try:
        if request.method == 'POST':
            print(request.form['birthdate'])
            print(datetime.strptime(request.form['birthdate'], '%Y-%m-%d'))
            birthdate = datetime.strptime(request.form['birthdate'], '%Y-%m-%d')
            new_res = Researcher(name=request.form['name'], surname=request.form['surname'],
                                 email=request.form['email'], birthdate=birthdate, password=request.form['password'],
                                 cv=request.files['cv'].read())
            adminSess.add(new_res)
            adminSess.commit()
            return redirect(url_for('login'))
        else:
            return render_template("registration.html")
    except Exception as e:
        print(e)
        adminSess.rollback()
    return Response(status=500)


@app.route('/login', methods=['GET', 'POST'])
def login():  # Funzione di login per l'autenticazione e l'accesso alla propria area riservata
    # riconosco metodo di richiesto come POST dal form html
    if request.method == 'POST':
        try:
            # Verifica se User è presente in db "USER"
            user = evSess.execute(select(User).where(User.email == request.form['email'])).fetchone()
            if user is None:  # Se lo user non esiste (credenziali sbagliate) viene incrementato il conto di ipBan
                ip_ban.add()
                return render_template('Login.html', login_error=True)
            adm = adminSess.execute(select(Admin).where(Admin.userUuid == user[0].uuid)).fetchone()
            ev = evSess.execute(select(Evaluator).where(Evaluator.userUuid == user[0].uuid)).fetchone()
            res = resSess.execute(select(Researcher).where(Researcher.userUuid == user[0].uuid)).fetchone()

            # Controlla se sta facendo login Admin
            if adm is not None:
                if adm.Admin.auth_pwd(request.form['password']):
                    login_user(adm.Admin)
                    return redirect(url_for('admin_route.admin'))
                else:
                    return render_template('Login.html', login_error=True)
            elif ev is not None:
                # Controlla se login è di tipo Evaluator
                ev = ev.Evaluator
                if ev.auth_pwd(request.form['password']):
                    login_user(ev)
                    return redirect(url_for('eval_route.eval_page'))
                else:
                    return render_template('Login.html', login_error=True)
            elif res is not None:
                # controlla se login è di tipo Researcher
                res = res.Researcher
                if res.auth_pwd(request.form['password']):
                    login_user(res)
                    return redirect(url_for('res_route.res_private'))
                else:
                    return render_template('Login.html', login_error=True)
            else:
                return render_template('Login.html', login_error=True)
        except Exception as e:
            print(e)
            evSess.rollback()
        return render_template("Login.html")
    else:
        if current_user.is_authenticated:  # Se l'utente è ancora autenticato nella sessione viene reinderizzato alla
            # propria area privata
            if isinstance(current_user, Admin):
                return redirect(url_for('admin_route.admin'))
            elif isinstance(current_user, Evaluator):
                return redirect(url_for('eval_route.eval_page'))
            else:
                return redirect(url_for('res_route.res_private'))
        else:
            return render_template('Login.html')


@app.route('/logout')
@login_required
def logout():  # Funzione di logout che reindirizza alla pagina di registrazione
    logout_user()
    return redirect(url_for('registration'))


if __name__ == '__main__':
    # populate_database()
    app.run()
