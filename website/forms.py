from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class QuestionnaireForm(FlaskForm):
    question1 = StringField('Question 1', validators=[DataRequired()])
    question2 = StringField('Question 2', validators=[DataRequired()])
    question3 = StringField('Question 3', validators=[DataRequired()])
    submit = SubmitField('Submit')