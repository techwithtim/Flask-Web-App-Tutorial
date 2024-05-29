from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.validators import DataRequired

class QuestionnaireForm(FlaskForm):
    question1 = RadioField('Question 1', choices=[('option1', 'Option 1'), ('option2', 'Option 2'), ('option3', 'Option 3')], validators=[DataRequired()])
    question2 = RadioField('Question 2', choices=[('option1', 'Option 1'), ('option2', 'Option 2'), ('option3', 'Option 3')], validators=[DataRequired()])
    question3 = RadioField('Question 3', choices=[('option1', 'Option 1'), ('option2', 'Option 2'), ('option3', 'Option 3')], validators=[DataRequired()])
    submit = SubmitField('Submit')
