from flask import *
from flask_login import *
from sqlalchemy import *
from db import adminSess, resSess, evSess
from classes.admin import Admin
from classes.researcher import Researcher
from classes.evaluators import Evaluator
from classes.user import User


app = Flask(__name__)
app.config['SECRET_KEY'] = 'askh7-wur0z!'
login_manager = LoginManager()
login_manager.init_app(app)

# todo: controllare cos'è
# ip_ban = IpBan(ban_count=5)
# ip_ban.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    admin = adminSess.execute(select(Admin).where(Admin.uuid == user_id)).fetchone()
    if admin is not None:
        return admin.Admin
    # todo: chiedere elia perchè messo user = teacherSession(...)
    evaluator = evSess.execute(select(Evaluator).where(Evaluator.userUuid == user_id)).fetchone().Evaluator
    if evaluator is not None:
        return Evaluator
    researcher = resSess.execute(select(Researcher).where(Researcher.userUuid == user_id)).fetchone().Researcher
    if researcher is not None:
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
                if adm.Admin.auth_pwd(request.form['password']):
                    login_user(adm.Admin)
                else:
                    return render_template('home.html', login_error=True)
            elif ev is not None:
                ev = ev.Evaluator
                if ev.auth_pwd(request.form['password']):
                    login_user(ev)
                    return redirect(url_for('/private'))
                else:
                    return render_template('home.html', login_error=True)
            elif res is not None:
                res = res.Researcher
                if res.auth_pwd(request.form['password']):
                    login_user(res)
                    return redirect(url_for('/private'))
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
            return redirect(url_for('/private'))
        else:
            return render_template('home.html')


'''@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        conn = engine.connect()
        #query = select(users.c.pwd).where(users.c.email == request.form['user'])
        #rs = conn.execute(query)
        #real_pwd = rs.fetchone()
        conn.close()
    if real_pwd is not None:
            if request.form['pass'] == real_pwd.pwd:
                user = load_user(request.form('user'))
                login_user(user)
                return redirect(url_for('private'))
            else:
                return redirect(url_for('home_page'))
        else:
            return redirect(url_for('home_page'))
    else:
        return redirect(url_for('home_page'))
    return redirect(url_for('home'))'''


'''@app.route('/register')
def reg():
    return render_template("registration.html")


@app.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home_page'))


@app.route('/registration', methods=['GET', 'POST'])
def register():
    if current_user.is_anonymous:
        return render_template('registration.html')
    elif current_user.is_authenticated:
        return redirect(url_for('private'))'''


@app.route('/private')
@login_required
def private():
    return render_template("private.html")


'''@app.route('/new_user', methods = ['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        conn.engine = engine.connect()
        mail = request.form['email']
        password = request.form['password']
        sel = select(users).where(users.c.email == mail);
        res = conn.execute(sel)
        res = res.fetchone()
        if res is None:
            ins = insert(users).values(email=mail, pwd=password)
            conn.execute(ins)
            conn.commit()
        return redirect(url_for('home_page'))'''

if __name__ == '__main__':
    app.run()
