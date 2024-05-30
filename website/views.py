from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_required, current_user
from .forms import InitialQuestionForm, create_dynamic_form
from .models import QuestionnaireResponse

# Initialize the Blueprint
views = Blueprint('views', __name__)

# Sample nested questions data
questions_data = {
    '1': {
        'text': 'Are there any muscle groups you DO NOT want to exercise?',
        'choices': [('1', 'Yes'), ('2', 'No')],
        'next': {
            '1': '1.1',  # Follow-up questions for answer '1'
            '2': 'end'   # Redirect to workout split for answer '2'
        }
    },
    '1.1': {
        'text': 'Select all muscle groups you DO NOT want to exercise',
        'choices': [('A', 'Chest'), ('B', 'Back'), ('C', 'Arms'), ('D', 'Shoulders'), ('E', 'Legs')],
        'multi': True,
        'next': {
            'A': 'end',
            'B': 'end',
            'C': 'end',
            'D': 'end',
            'E': 'end'
        }
    },
    '1.1.1': {
        'text': 'Follow-up Question 1.1.1: [Placeholder]',
        'choices': [('X', 'X'), ('Y', 'Y'), ('Z', 'Z')],
        'next': {}
    },
    # ... other questions ...
}

@views.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
    form = InitialQuestionForm()
    if form.validate_on_submit():
        days = form.days.data
        session['days'] = days
        session['current_question'] = '1'  # Start with question id '1'
        session['history'] = []  # Initialize history
        session['responses'] = {}  # Initialize responses
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
                session['responses'][current_question_id] = answer
                if isinstance(answer, list):
                    # Handle multi-select answers
                    next_question_id = question['next'].get(answer[0], None)  # Choose appropriate logic for multi-select
                else:
                    next_question_id = question['next'].get(answer, None)
                if next_question_id == 'end':
                    return redirect(url_for('views.split'))  # Redirect to workout split tab at the end of the branch
                elif next_question_id:
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
    
    return render_template('dynamic_question.html', question=question, form=form)

@views.route('/', methods=['GET'])
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/split', methods=['GET'])
@login_required
def split():
    # Use session['responses'] to customize the workout split
    responses = session.get('responses', {})
    # Process responses to customize the workout split
    return render_template("split.html", user=current_user, responses=responses)

@views.route('/tracker', methods=['GET'])
@login_required
def tracker():
    return render_template("tracker.html", user=current_user)

@views.route('/weight_tracker', methods=['GET'])
@login_required
def weight_tracker():
    return render_template("weight_tracker.html", user=current_user)
