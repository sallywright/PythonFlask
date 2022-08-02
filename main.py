"""
Uzduotys:
1.(3) Surasti, isvardinti ir pataisyti visas projekte rastas klaidas zemiau, uz bent 5 rastas ir pataisytas pilnas balas:
    a)
    Klaida:
        User schemoje yra "last_name" stulpelis, kuris nera nullable bet taip pat ir formoje nera renkama tokia informacija.
        Del to, registruojantis meta klaida, nes vietoj "last_name" paduodamas None boolean. 
    Pataisymas:
        sign_up.html formoje prideta skiltis ivesti "last_name".
        "sign_up" route pridetas last name parametras User schemai.
        "SignUpForm" formoje pridetas last name parametras.
    b)
    Klaida:
        User schemoje nebuvo skilties "is_active" reikalingos user_login'ui.
        Del to, registruojantis meta klaida, kad User objektas neturi "is_active" atributo.
    Pataisymas:
        "User" schemai pridetas "is_active" atributas, kuris default'ina i True boolen'a.
    c)
    Klaida:
    User schema nepaveldi UserMixin klases.
    Del to, prisijungiant meta klaida, kad nera "get_id" metodo. 
    d)
    Klaida:
    "sign_in" route'e Useris yra filtruojamas lyginant first_name su e-mail address. 
    Pataisymas:
    Pakeista kad e-mail address lygintu su e-mail address.

    e)
    Klaida:
    "sign_in" route'as neturejo metodu ["POST", "GET"]
    Pataisymas:
    "sign_in" route'e prideti metodai ["POST", "GET"]

    f)
    Klaida:
    update_account_information.html template'e vietoj "form" buvo naudojamas "form_in_html" variable, kuris nebuvo nurodytas renderinant template'a
    Pataisymas:
    update_account_information.html template'e "form_in_html" pervadintas i "form".

    g)
    Klaida:
    log_out route'e nera logout_user() funkcijos.
    Del to, logout'as faktiskai neislogoutina userio.
    Pataisymas:
    pridetas logout_user import'as.
    prideta logout_user() funkcija "log_out" route'e.

    h)
    Klaida:
    "User" schemoje first name data type buvo integer.
    Pataisymas:
    Pakeista i string.

    ...
2.(7) Praplesti aplikacija i bibliotekos resgistra pagal apacioje surasytus reikalavimus:
    a)(1) Naudojant SQLAlchemy klases, aprasyti lenteles Book, Author su pasirinktinais atributais su tinkamu rysiu -
        vienas autorius, gali buti parases daug knygu, ir uzregistruoti juos admin'e
    b)(2) Sukurti (papildomus) reikiamus rysius tarp duombaziniu lenteliu, kad atitiktu zemiau pateiktus reikalavimus
    c) Sukurti puslapius Available Books ir My Books:
        i)(2) Available Books puslapis
            - isvesti bent knygos pavadinima ir autoriu
            - turi buti prieinamas tik vartotojui prisijungus,
            - rodyti visas knygas, kurios nera pasiskolintos
            - tureti mygtuka ar nuoroda "Borrow" prie kiekvienos knygos, kuri/ia paspaudus, knyga yra priskiriama
              varototojui ir puslapis perkraunamas
              (del paprastumo, sakome kad kiekvienos i sistema suvestos knygos turima lygiai 1)
        ii)(2) My Books puslapis
            - turi matytis ir buti prieinamas tik vartotojui prisijungus
            - rodyti visas knygas, kurios yra pasiskolintos prisijungusio vartotojo
            - salia kiekvienos knygos mygtuka/nuoroda "Return", kuri/ia paspaudus, knyga grazinama i biblioteka ir
              perkraunamas puslapis
    f)(2) Bonus: praplesti aplikacija taip, kad bibliotekoje kiekvienos knygos galetu buti
        daugiau negu vienas egzempliorius
Pastabos:
    - uzstrigus su pirmaja uzduotimi, galima paimti musu paskutini flask projekto template
        ir ten atlikti antra uzduoti
    - nereikalingus templates geriau panaikinti ar persidaryti, kaip reikia. Tas pats galioja su MyTable klase
    - antram vartotojui prisijungus, nebeturi matytis kyngos, kurios buvo pasiskolintos pirmojo vartotojo
        nei prie Available Books, nei prie My Books
    - visam administravimui, pvz. knygu suvedidimui galima naudoti admin
    - sprendziant bonus uzduoti, apsvarstyti papildomos lenteles isivedima
"""

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_bcrypt import Bcrypt
from flask_login import (
    AnonymousUserMixin,
    UserMixin,
    LoginManager,
    login_user,
    current_user,
    login_required,
    logout_user,
)
from flask_sqlalchemy import SQLAlchemy
import forms
import json

app = Flask(__name__)


class MyAnonymousUserMixin(AnonymousUserMixin):
    is_admin = False


login_manager = LoginManager(app)

login_manager.login_view = "sign_in"
login_manager.login_message = "Please login to access this page."
login_manager.login_message_category = "info"
login_manager.anonymous_user = MyAnonymousUserMixin

admin = Admin(app)

bcrypt = Bcrypt(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.sqlite?check_same_thread=False"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = '(/("ZOHDAJK)()kafau029)ÖÄ:ÄÖ:"OI§)"Z$()&"()!§(=")/$'

db = SQLAlchemy(app)


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email_address = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)


class Book(db.Model):
    __tablename__ = "book"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


db.create_all()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    form = forms.SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password1.data).decode()
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email_address=form.email_address.data,
            password=hashed_password,
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(f"Welcome, {current_user.first_name}", "success")
        return redirect(url_for("home"))
    return render_template("sign_up.html", form=form)


@app.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    form = forms.SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email_address=form.email_address.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f"Welcome, {current_user.first_name}", "success")
            return redirect(request.args.get("next") or url_for("home"))
        flash(f"User or password does not match", "danger")
        return render_template("sign_in.html", form=form)
    return render_template("sign_in.html", form=form)


@app.route("/update_account_information", methods=["GET", "POST"])
@login_required
def update_account_information():
    form = forms.UpdateAccountInformationForm()
    if request.method == "POST":
        form.email_address.data = current_user.email_address
        form.first_name.data = current_user.email_address
        form.last_name.data = current_user.email_address
    if form.validate_on_submit():
        current_user.email_address = form.email_address.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        db.session.commit()
        flash("User information updated", "success")
        return redirect(url_for("update_account_information"))
    return render_template("update_account_information.html", form=form)


@app.route("/sign_out")
def sign_out():
    logout_user()
    flash("Goodbye, see you next time", "success")
    return render_template("home.html")


# ----------------------------------------------------------------------------------------------------------------------
# Library routes
# ----------------------------------------------------------------------------------------------------------------------


@app.route("/add_book", methods=["GET", "POST"])
@login_required
def add_book():
    form = forms.BookAdditionForm()
    if form.validate_on_submit():
        book = Book(
            title=form.title.data,
            author=form.author.data,
        )
        db.session.add(book)
        db.session.commit()
        return render_template("success.html")
    return render_template("add_form.html", form=form)


@app.route("/my_reserved_books", methods=["GET", "POST"])
@login_required
def get_reserved_books():
    requester_user_id = current_user.id
    reserved_books = Book.query.filter_by(user_id=requester_user_id).all()
    return render_template("owned_books.html", data=reserved_books)


@app.route("/my_reserved_books/<id>", methods=["DELETE"])
@login_required
def delete_reserved_book(id):
    requester_user_id = current_user.id
    book = Book.query.filter_by(id=id, user_id=requester_user_id).first()
    print("book")
    print(book)
    if book:
        book.user_id = None
        db.session.commit()
        return app.response_class(
            response=json.dumps({"ok": True}), status=200, mimetype="application/json"
        )
    return app.response_class(
        response=json.dumps({"ok": False}), status=403, mimetype="application/json"
    )


@app.route("/reserve_book", methods=["GET"])
@login_required
def get_reservations():
    available_books = Book.query.filter_by(user_id=None).all()
    return render_template("available_books.html", data=available_books)


@app.route("/reserve_book/<id>", methods=["POST"])
@login_required
def add_reservations(id):
    requester_user_id = current_user.id
    book = Book.query.filter_by(id=id).first()
    print("book")
    print(book)
    if book:
        book.user_id = requester_user_id
        db.session.commit()
        return app.response_class(
            response=json.dumps({"ok": True}), status=201, mimetype="application/json"
        )
    return app.response_class(
        response=json.dumps({"ok": False}), status=403, mimetype="application/json"
    )


# ----------------------------------------------------------------------------------------------------------------------
# Library routes
# ----------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    app.run(debug=True)
