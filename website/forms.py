from flask_wtf import FlaskForm
from wtforms import RadioField, SelectMultipleField, SubmitField
from wtforms.widgets import ListWidget, CheckboxInput

class InitialQuestionForm(FlaskForm):
    days = RadioField('How many days a week do you want to workout?', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7')], coerce=int)
    submit = SubmitField('Next')

def create_dynamic_form(question):
    class DynamicForm(FlaskForm):
        if question.get('multi'):
            answer = SelectMultipleField(question['text'], choices=question['choices'], option_widget=CheckboxInput(), widget=ListWidget(prefix_label=False))
        else:
            answer = RadioField(question['text'], choices=question['choices'], coerce=str)
        submit = SubmitField('Next')
    return DynamicForm
