from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                if not user.has_completed_questionnaire:
                    return redirect(url_for('views.questionnaire'))
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password')
        else:
            flash('Email does not exist')
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already exists')
            return redirect(url_for('auth.sign_up'))

        if password1 != password2:
            flash('Passwords do not match')
            return redirect(url_for('auth.sign_up'))

        new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='pbkdf2:sha256', salt_length=8))

        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)

        return redirect(url_for('views.questionnaire'))

    return render_template('sign_up.html')
