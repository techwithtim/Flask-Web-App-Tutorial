from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_required, current_user
from .forms import InitialQuestionForm, create_dynamic_form
from .models import QuestionnaireResponse

# Initialize the Blueprint
views = Blueprint('views', __name__)

# Sample nested questions data
questions_data = {
    '1': {
        'text': 'Question 2: How many times a week do you want to do cardio?',
        'choices': [('1', '1'), ('2', '2'), ('3', '3')],
        'next': {
            '1': '1.1',  # Follow-up questions for answer '1'
            '2': '1.2',  # Follow-up questions for answer '2'
            '3': '1.3'   # Follow-up questions for answer '3'
        }
    },
    '1.1': {
        'text': 'Follow-up Question 1.1: [Placeholder]',
        'choices': [('A', 'A'), ('B', 'B'), ('C', 'C')],
        'next': {
            'A': '1.1.1',
            'B': '1.1.2',
            'C': '1.1.3'
        }
    },
    '1.2': {
        'text': 'Follow-up Question 1.2: [Placeholder]',
        'choices': [('A', 'A'), ('B', 'B'), ('C', 'C')],
        'next': {
            'A': '1.2.1',
            'B': '1.2.2',
            'C': '1.2.3'
        }
    },
    '1.3': {
        'text': 'Follow-up Question 1.3: [Placeholder]',
        'choices': [('A', 'A'), ('B', 'B'), ('C', 'C')],
        'next': {
            'A': '1.3.1',
            'B': '1.3.2',
            'C': '1.3.3'
        }
    },
    '1.1.1': {
        'text': 'Follow-up Question 1.1.1: [Placeholder]',
        'choices': [('X', 'X'), ('Y', 'Y'), ('Z', 'Z')],
        'next': {}
    },
    '1.1.2': {
        'text': 'Follow-up Question 1.1.2: [Placeholder]',
        'choices': [('X', 'X'), ('Y', 'Y'), ('Z', 'Z')],
        'next': {}
    },
    '1.1.3': {
        'text': 'Follow-up Question 1.1.3: [Placeholder]',
        'choices': [('X', 'X'), ('Y', 'Y'), ('Z', 'Z')],
        'next': {}
    },
    '1.2.1': {
        'text': 'Follow-up Question 1.2.1: [Placeholder]',
        'choices': [('X', 'X'), ('Y', 'Y'), ('Z', 'Z')],
        'next': {}
    },
    '1.2.2': {
        'text': 'Follow-up Question 1.2.2: [Placeholder]',
        'choices': [('X', 'X'), ('Y', 'Y'), ('Z', 'Z')],
        'next': {}
    },
    '1.2.3': {
        'text': 'Follow-up Question 1.2.3: [Placeholder]',
        'choices': [('X', 'X'), ('Y', 'Y'), ('Z', 'Z')],
        'next': {}
    },
    '1.3.1': {
        'text': 'Follow-up Question 1.3.1: [Placeholder]',
        'choices': [('X', 'X'), ('Y', 'Y'), ('Z', 'Z')],
        'next': {}
    },
    '1.3.2': {
        'text': 'Follow-up Question 1.3.2: [Placeholder]',
        'choices': [('X', 'X'), ('Y', 'Y'), ('Z', 'Z')],
        'next': {}
    },
    '1.3.3': {
        'text': 'Follow-up Question 1.3.3: [Placeholder]',
        'choices': [('X', 'X'), ('Y', 'Y'), ('Z', 'Z')],
        'next': {}
    }
    # Add more questions as needed
}

@views.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
    form = InitialQuestionForm()
    if form.validate_on_submit():
        days = form.days.data
        session['days'] = days
        session['current_question'] = '1'  # Start with question id '1'
        session['history'] = []  # Initialize history
        return redirect(url_for('views.dynamic_question'))
    return render_template('questionnaire.html', form=form)

@views.route('/dynamic_question', methods=['GET', 'POST'])
def dynamic_question():
    current_question_id = session.get('current_question')
    if current_question_id is None:
        return redirect(url_for('views.questionnaire'))
    
    question = questions_data.get(current_question_id)
    if question is None:
        return redirect(url_for('views.questionnaire'))  # Redirect to start if question not found
    
    DynamicForm = create_dynamic_form(question)
    form = DynamicForm()

    if request.method == 'POST':
        if 'next' in request.form:
            if form.validate():
                answer = form.answer.data
                next_question_id = question['next'].get(answer)
                if next_question_id:
                    session['history'].append(current_question_id)
                    session['current_question'] = next_question_id
                    return redirect(url_for('views.dynamic_question'))
                else:
                    return redirect(url_for('views.questionnaire'))  # Redirect to start if no next question
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
    return render_template("split.html", user=current_user)

@views.route('/tracker', methods=['GET'])
@login_required
def tracker():
    return render_template("tracker.html", user=current_user)
