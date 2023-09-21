from flask import Blueprint, render_template, request, flash, redirect, url_for
from .views import User
from .views import users
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import json
from re import fullmatch,compile

########################################################################################

auth = Blueprint('auth', __name__)

def load_user_data_from_file(email):
    with open('users.json', 'r') as file:   
        users_data = json.load(file)
        return users_data.get(email)

 ########################################################################################

@auth.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if email in users:
            user = users[email]
            if user.password == password:
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home')) #takes us to the home.html page 
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

###################################################################################################

@auth.route('/logout/')  #is used to bind a function to a URL.
@login_required 
def logout():
    logout_user() 
    return redirect(url_for('auth.login'))

regex = compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

def isValid(email):
    if fullmatch(regex, email):
      return True
    else:
      return False

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        

        existing_user = User.query.filter_by(email=email).first()
        if isValid(existing_user):
            flash("Correct Email")
        else :
            flash("Incorrect Email")
        if existing_user:
            flash('Email already exists. Please log in.', category='error')
            return redirect(url_for('auth.login'))
        
        else:
            new_user = User(email=email, name=name, password=generate_password_hash(
                password1, method='sha256'))
            login_user(new_user, remember=True)
            flash('Account created successfully!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
