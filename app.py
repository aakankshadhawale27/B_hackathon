import io
from werkzeug.utils import secure_filename
import os
from flask import Flask, render_template, session, url_for, redirect, request
import csv
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
import sqlite3
from flask_bcrypt import Bcrypt

connection = sqlite3.connect('E:\Flask_signup_login\database.db')
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
with app.app_context():
    db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    # name = db.Column(db.String(100))
    # data = db.Column(db.LargeBinary)


class Registerform(FlaskForm):
    username = StringField(validators=[
        InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[
        InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class Loginform(FlaskForm):
    username = StringField(validators=[
        InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[
        InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Loginform()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)
    # return render_template('login.html')


# @app.route('/upload', methods=['POST'])
# def upload():
#     file = request.files['file']
#     if not file:
#         return "No file selected"
#     data = []
#     stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
#     csv_input = csv.reader(stream)
#     for row in csv_input:
#         data.append(row)
#     return render_template('result.html', data=data)


@app.route('/dashboard', methods=['GET', 'POST'])
# @login_required
def dashboard():
    # file = request.files['file']
    # if not file:
    #     return "No file selected"
    # data = []
    # stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
    # csv_input = csv.reader(stream)
    # for row in csv_input:
    #     data.append(row)
    # return render_template('login.html', data=data)
    # if request.method == 'POST':
    #     file = request.files['file']
    #     new_file = open(name=file.filename, data=file.read())
    #     db.session.add(new_file)
    #     db.session.commit()
    #     return 'File uploaded successfully'
    return render_template('dashboard.html')


# @app.route('/', methods=['GET', 'POST'])
# def uploadFile():
#     if request.method == 'POST':
#       # upload file flask
#         f = request.files.get('file')

#         # Extracting uploaded file name
#         data_filename = secure_filename(f.filename)

#         f.save(os.path.join(app.config['UPLOAD_FOLDER'], data_filename))

#         session['uploaded_data_file_path'] = os.path.join(
#             app.config['UPLOAD_FOLDER'], data_filename)

#         return render_template('login.html')
#     return render_template("index.html")


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = Registerform()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('dashboard'))

    return render_template('signup.html', form=form)


if __name__ == '__main__':
    app.run()
