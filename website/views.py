from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, flash
from flask_login import login_required, current_user
from .models import User, Weight, QuestionnaireResponse
from . import db
from .questionnaire import questions_data, conditions_messages, get_next_question_and_update_session, initialize_questionnaire, get_question_and_form

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template('home.html', user=current_user)

@views.route('/about')
def about():
    return render_template('about.html')

@views.route('/questionnaire', methods=['GET', 'POST'])
@login_required
def questionnaire():
    if current_user.has_completed_questionnaire:
        return redirect(url_for('views.home'))

    form = InitialQuestionForm()
    if form.validate_on_submit():
        if initialize_questionnaire(form):
            return redirect(url_for('views.dynamic_question'))
    return render_template('questionnaire.html', form=form)

@views.route('/dynamic_question', methods=['GET', 'POST'])
@login_required
def dynamic_question():
    if current_user.has_completed_questionnaire:
        return redirect(url_for('views.home'))

    question, form = get_question_and_form()
    if question is None:
        return redirect(url_for('views.questionnaire'))

    if request.method == 'POST':
        if 'next' in request.form and form.validate():
            answer = request.form.get('answer')
            next_question_id = get_next_question_and_update_session(answer, question)
            if next_question_id is None:
                current_user.has_completed_questionnaire = True
                db.session.commit()
                return redirect(url_for('views.home'))
            return redirect(url_for('views.dynamic_question'))
        elif 'back' in request.form:
            if session['history']:
                previous_question_id = session['history'].pop()
                session['current_question'] = previous_question_id
                return redirect(url_for('views.dynamic_question'))
            else:
                return redirect(url_for('views.questionnaire'))

    return render_template('dynamic_question.html', question=question, form=form)

@views.route('/split', methods=['GET'])
@login_required
def split():
    responses = session.get('responses', {})
    condition = session.get('condition', 'condition1')
    days = session.get('days', 0)
    muscle_groups = {
        'A': 'Chest',
        'B': 'Back',
        'C': 'Arms',
        'D': 'Shoulders',
        'E': 'Legs'
    }
    excluded_groups = responses.get('1.1', [])
    included_groups = [muscle_groups[key] for key in muscle_groups if key not in excluded_groups]
    message = conditions_messages.get(condition, 'Default message')

    return render_template("split.html", user=current_user, included_groups=included_groups, days=days, message=message)

@views.route('/weight_tracker', methods=['GET', 'POST'])
@login_required
def weight_tracker():
    if request.method == 'POST':
        weight = request.form.get('weight')
        if weight:
            new_weight = Weight(weight=float(weight), user_id=current_user.id)
            db.session.add(new_weight)
            db.session.commit()
    weights = Weight.query.filter_by(user_id=current_user.id).order_by(Weight.date).all()
    return render_template("weight_tracker.html", user=current_user, weights=weights)

@views.route('/get_weights')
@login_required
def get_weights():
    weights = Weight.query.filter_by(user_id=current_user.id).order_by(Weight.date).all()
    weights_data = [{"date": w.date.strftime("%Y-%m-%d"), "weight": w.weight} for w in weights]
    return jsonify(weights_data)

@views.route('/get_todays_workout')
@login_required
def get_todays_workout():
    todays_workout = "Chest: bench press 3 x 10, lateral raise 4 x 15, tricep pushdowns 3 x 12, dips 3 x 15."
    return jsonify({"todays_workout": todays_workout})

