from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField

class InitialQuestionForm(FlaskForm):
    days = RadioField('How many days a week do you want to workout?', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7')], coerce=int)
    submit = SubmitField('Next')

class SecondQuestionForm(FlaskForm):
    submit = SubmitField('Next')
