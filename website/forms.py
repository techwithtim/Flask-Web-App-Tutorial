from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.validators import DataRequired

class QuestionnaireForm(FlaskForm):
    question1 = RadioField('How many days a week would you like to workout?', choices=[('option1', '1'), ('option2', '2'), ('option3', '3'), 
                                                                                       ('option4', '4'), ('option5', '5'), 
                                                                                       ('option6', '6'), ('option7', '7')], validators=[DataRequired()])
    question2 = RadioField('What body parts would you NOT like to exercise?', choices=[('option1', 'Chest'), ('option2', 'Back'), ('option3', 'Arms')
                                                                                       , ('option4', 'Shoulders'), ('option5', 'Legs')], validators=[DataRequired()])
    question3 = RadioField('Which body part would you like to focus on?', choices=[('option1', 'Chest'), ('option2', 'Back'), ('option3', 'Arms')
                                                                                       , ('option4', 'Shoulders'), ('option5', 'Legs')], validators=[DataRequired()])
    submit = SubmitField('Submit')
