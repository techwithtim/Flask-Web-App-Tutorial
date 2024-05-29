from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import QuestionnaireResponse
from .forms import QuestionnaireForm
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/questionnaire', methods=['GET', 'POST'])
@login_required
def questionnaire():
    form = QuestionnaireForm()
    if form.validate_on_submit():
        response = QuestionnaireResponse(
            user_id=current_user.id,
            question1=form.question1.data,
            question2=form.question2.data,
            question3=form.question3.data
        )
        db.session.add(response)
        db.session.commit()
        flash('Thank you for completing the questionnaire!', 'success')
        return redirect(url_for('views.questionnaire'))

    return render_template("questionnaire.html", user=current_user, form=form)

@views.route('/split', methods=['GET'])
@login_required
def split():
    return render_template("split.html", user=current_user)
