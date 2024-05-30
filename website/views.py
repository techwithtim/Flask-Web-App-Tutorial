from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, current_user
from .models import QuestionnaireResponse
from . import db
from .forms import InitialQuestionForm, SecondQuestionForm

# Initialize the Blueprint
views = Blueprint('views', __name__)

# Define the routes within the Blueprint
@views.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
    form = InitialQuestionForm()
    if form.validate_on_submit():
        days = form.days.data
        session['days'] = days
        return redirect(url_for('views.question2'))
    return render_template('questionnaire.html', form=form)

@views.route('/question2', methods=['GET', 'POST'])
def question2():
    days = session.get('days')
    if days is None:
        return redirect(url_for('views.questionnaire'))
    form = SecondQuestionForm()
    if form.validate_on_submit():
        # Process the form data and redirect to the next question or a results page
        return redirect(url_for('views.questionnaire'))  # For now, redirect back to the start
    return render_template('question2.html', days=days, form=form)

@views.route('/', methods=['GET'])
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/split', methods=['GET'])
@login_required
def split():
    return render_template("split.html", user=current_user)

@views.route('/tracker', methods=['GET'])
@login_required
def tracker():
    return render_template("tracker.html", user=current_user)

@views.route('/weight_tracker', methods=['GET'])
@login_required
def weight_tracker():
    return render_template("weight_tracker.html", user=current_user)
