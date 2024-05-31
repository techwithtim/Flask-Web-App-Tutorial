from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, flash
from flask_login import login_required, current_user
from .forms import InitialQuestionForm, create_dynamic_form
from .models import User, Weight
from . import db

views = Blueprint('views', __name__)

questions_data = {
    '1': {
        'text': 'Are there any muscle groups you DO NOT want to exercise?',
        'choices': [('1', 'Yes'), ('2', 'No')],
        'next': {
            '1': '1.1',
            '2': 'end_condition1'
        }
    },
    '1.1': {
        'text': 'Select all muscle groups you DO NOT want to exercise',
        'choices': [('A', 'Chest'), ('B', 'Back'), ('C', 'Arms'), ('D', 'Shoulders'), ('E', 'Legs')],
        'multi': True,
        'next': {
            'A': 'end_condition2',
            'B': 'end_condition2',
            'C': 'end_condition2',
            'D': 'end_condition2',
            'E': 'end_condition2'
        }
    },
    '2': {
        'text': 'How many days a week do you want to workout?',
        'choices': [('1', '1 day'), ('2', '2 days'), ('3', '3 days'), ('4', '4 days'), ('5', '5 days'), ('6', '6 days'), ('7', '7 days')],
        'next': {
            '1': '2.1',
            '2': 'end_condition3'
        }
    },
    '2.1': {
        'text': 'Do you want to workout on back to back days?',
        'choices': [('1', 'Yes'), ('2', 'No')],
        'next': {
            '1': 'end_condition3',
            '2': 'end_condition3'
        }
    }
}

conditions_messages = {
    'condition1': 'Message for condition 1',
    'condition2': 'Message for condition 2',
    'condition3': 'Message for condition 3'
}

@views.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
    form = InitialQuestionForm()
    if form.validate_on_submit():
        selected_option = form.days.data
        if selected_option:
            flash(f'You selected: {selected_option}')
            session['days'] = selected_option
            session['current_question'] = '1'  # Assuming the first question is '1'
            session['history'] = []
            session['responses'] = {}
            return redirect(url_for('views.dynamic_question'))
    return render_template('questionnaire.html', form=form)

@views.route('/dynamic_question', methods=['GET', 'POST'])
def dynamic_question():
    current_question_id = session.get('current_question')
    if current_question_id is None:
        return redirect(url_for('views.questionnaire'))
    
    question = questions_data.get(current_question_id)
    if question is None:
        return redirect(url_for('views.questionnaire'))
    
    DynamicForm = create_dynamic_form(question)
    form = DynamicForm()

    if request.method == 'POST':
        if 'next' in request.form:
            if form.validate():
                answer = request.form.get('answer')
                if question.get('multi'):
                    answer = answer.split(',')
                else:
                    answer = [answer]
                session['responses'][current_question_id] = answer
                
                # Determine the next question or end condition based on all selected answers
                next_question_id = None
                for ans in answer:
                    next_id = question['next'].get(ans)
                    if next_id and next_id.startswith('end_condition'):
                        session['condition'] = next_id.replace('end_', '')
                        return redirect(url_for('views.split'))
                    elif next_id:
                        next_question_id = next_id

                if next_question_id:
                    session['history'].append(current_question_id)
                    session['current_question'] = next_question_id
                    return redirect(url_for('views.dynamic_question'))
                else:
                    return redirect(url_for('views.questionnaire'))
        elif 'back' in request.form:
            if session['history']:
                previous_question_id = session['history'].pop()
                session['current_question'] = previous_question_id
                return redirect(url_for('views.dynamic_question'))
            else:
                return redirect(url_for('views.questionnaire'))
    
    return render_template('dynamic_question.html', question=question, form=form)

@views.route('/', methods=['GET'])
@login_required
def home():
    return render_template("home.html", user=current_user)

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

@views.route('/tracker', methods=['GET'])
@login_required
def tracker():
    return render_template("tracker.html", user=current_user)

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
