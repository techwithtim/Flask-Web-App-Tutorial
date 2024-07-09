from flask import session
from .forms import InitialQuestionForm, create_dynamic_form

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

def get_next_question_and_update_session(answer, question):
    next_question_id = None
    if question.get('multi'):
        answer = answer.split(',')
    else:
        answer = [answer]
    session['responses'][session['current_question']] = answer

    for ans in answer:
        next_id = question['next'].get(ans)
        if next_id and next_id.startswith('end_condition'):
            session['condition'] = next_id.replace('end_', '')
            return None  # End condition reached
        elif next_id:
            next_question_id = next_id
    
    if next_question_id:
        session['history'].append(session['current_question'])
        session['current_question'] = next_question_id

    return next_question_id

def initialize_questionnaire(form):
    selected_option = form.days.data
    if selected_option:
        session['days'] = selected_option
        session['current_question'] = '1'  # Assuming the first question is '1'
        session['history'] = []
        session['responses'] = {}
        return True
    return False

def get_question_and_form():
    current_question_id = session.get('current_question')
    if current_question_id is None:
        return None, None

    question = questions_data.get(current_question_id)
    if question is None:
        return None, None

    DynamicForm = create_dynamic_form(question)
    form = DynamicForm()
    return question, form
