from flask import *
from flask_login import *
from sqlalchemy import *
from db import adminSess, resSess, evSess
from classes.admin import Admin
from classes.researcher import Researcher
from classes.evaluators import Evaluator
from classes.user import User
from testing import testing


app = Flask(__name__)
app.config['SECRET_KEY'] = 'askh7-wur0z!'
login_manager = LoginManager()
login_manager.init_app(app)
testing()


# todo: controllare cos'è
# ip_ban = IpBan(ban_count=5)
# ip_ban.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    admin = adminSess.execute(select(Admin).where(Admin.uuid == user_id)).fetchone()
    if admin is not None:
        print('ho trovato Admin')
        return admin.Admin
    # todo: chiedere elia perchè messo user = teacherSession(...)
    evaluator = evSess.execute(select(Evaluator).where(Evaluator.userUuid == user_id)).fetchone().Evaluator
    if evaluator is not None:
        print('ho trovato evaluator')
        return Evaluator
    researcher = resSess.execute(select(Researcher).where(Researcher.userUuid == user_id)).fetchone().Researcher
    if researcher is not None:
        print('ho trovato researcher')
        return Researcher


@app.route('/')
def home():  # put application's code here
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            # Verifica se user è presente in db
            user = evSess.execute(select(User).where(User.email==request.form['email'])).fetchone()
            if user is None:
                return render_template('home.html', login_error=True)

            adm=adminSess.execute(select(Admin).where(Admin.userUuid == user[0].uuid)).fetchone()
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
                ev = ev.Evaluator
                print('ho trovato evaluator in login')
                if ev.auth_pwd(request.form['password']):
                    login_user(ev)
                    return redirect(url_for('private'))
                else:
                    return render_template('home.html', login_error=True)
            elif res is not None:
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


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()
