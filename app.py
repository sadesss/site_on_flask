from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from flask_migrate import Migrate
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    UserMixin,
    current_user,
)

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:IU6@localhost/baum"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = "login"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    roles = db.Column(db.String(255))


class UserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    group = db.Column(db.String(20))
    mail = db.Column(db.String(255), unique=True, nullable=False)


class Mero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mero = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    group = db.Column(db.String(20), nullable=False)
    mail = db.Column(db.String(100), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"))
    event = db.relationship("Event", back_populates="meros")


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)
    meros = db.relationship("Mero", back_populates="event")


migrate.init_app(app, db)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


def check_user_credentials(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        login_user(user)
        flash("Вы успешно вошли в систему!", "success")
        return True
    return False


@app.route("/")
def home():
    return render_template("base.html")


@app.route("/forgot")
def forgot():
    return render_template("lost_password.html")


@app.route("/reg")
def reg():
    return render_template("reg.html")


@app.route("/registration", methods=["POST"])
def registration():
    try:
        name = request.form.get("name")
        lastname = request.form.get("lastname")
        group = request.form.get("group")
        mail = request.form.get("mail")

        # Добавление данных пользователя в таблицу user_data
        user_data = UserData(name=name, lastname=lastname, group=group, mail=mail)
        db.session.add(user_data)
        db.session.commit()

        # Получение id нового пользователя
        user_id = user_data.id

        # Извлечение логина из почты (всё до символа @)
        login = mail.split("@")[0]

        # Запись пароля в открытом виде
        password = "baumanka"

        # Создание нового пользователя в таблице user
        new_user = User(id=user_id, username=login, password=password, roles="baseuser")

        # Добавление пользователя в базу данных
        db.session.add(new_user)
        db.session.commit()
        print("Регистрация успешна, переход на страницу login")
        return render_template("login.html")

    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/create_event", methods=["POST"])
@login_required
def create_event():
    if request.method == "POST":
        event_name = request.form.get("event_name")
        event_date = request.form.get("event_date")
        event_description = request.form.get("event_description")

        # Создаем новое мероприятие в базе данных
        new_event = Event(
            name=event_name, date=event_date, description=event_description
        )
        db.session.add(new_event)
        db.session.commit()

        flash("Мероприятие успешно создано", "success")

        # Получаем созданное мероприятие с базы данных
        created_event = Event.query.filter_by(name=event_name).first()

        # # Создаем пост для этого мероприятия
        # new_mero = Mero(
        #     mero=event_name,
        #     name=current_user.username,
        #     lastname=current_user.lastname,
        #     group=current_user.group,
        #     mail=current_user.mail,
        #     event_id=created_event.id,
        # )
        # db.session.add(new_mero)
        # db.session.commit()

        flash("Мероприятие успешно опубликовано", "success")

    return redirect(url_for("dashboard"))


@app.route("/lk")
@login_required
def lk():
    user1 = current_user
    user_data = UserData.query.get(current_user.id)
    if user1.roles == "admin":
        records = Mero.query.all()
        return render_template("adminlk.html", records=records)
    else:
        if user_data:
            name = user_data.name
            lastname = user_data.lastname
            group = user_data.group
            mail = user_data.mail

            if lastname and name and group and mail:
                return render_template(
                    "lk.html", lastname=lastname, name=name, group=group, mail=mail
                )
            else:
                flash("Ошибка: данные пользователя не найдены RHBYl.", "danger")
                return redirect(url_for("login"))
        else:
            flash("Данные пользователя не найдены в таблице UserData", "danger")
            return redirect(url_for("login"))


@app.route("/apply", methods=["GET", "POST"])
@login_required
def apply():
    if request.method == "POST":
        mero_text = request.form.get("mero_text")

        if current_user.roles == "baseuser":
            user_data = UserData.query.filter_by(id=current_user.id).first()

            if user_data:
                name = user_data.name
                lastname = user_data.lastname
                group = user_data.group
                mail = user_data.mail

            
                new_mero = Mero(
                    mero=mero_text, name=name, lastname=lastname, group=group, mail=mail
                )
                db.session.add(new_mero)
                db.session.commit()

                return render_template(
                    "apply.html", name=name, lastname=lastname, group=group, mail=mail
                )

    return render_template("apply.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if check_user_credentials(username, password):
            flash("Вы успешно вошли в систему!", "success")
            return redirect(url_for("dashboard"))
        else:
            error_message = "Ошибка входа. Проверьте свои учетные данные."
            flash(error_message, "danger")
            return render_template("err.html", error_message=error_message)

    message = request.args.get("message")
    return render_template("login.html", message=message)


@app.route("/dashboard")
@login_required
def dashboard():
    meros = Mero.query.all()
    events = Event.query.all()

    if current_user.is_authenticated:
        username = current_user.username
        return render_template("dashboard.html", username=username, events=events)
    else:
        name = user_data.name
        lastname = user_data.lastname
        group = user_data.group
        mail = user_data.mail

        return render_template(
            "dashboard.html",
            name=name,
            lastname=lastname,
            group=group,
            mail=mail,
        )
    return render_template(
        "dashboard.html", username=current_user.username, meros=meros, events=events
    )
    flash("Вы не вошли в систему", "danger")
    return redirect(url_for("login"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Вы успешно вышли из системы!", "success")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
