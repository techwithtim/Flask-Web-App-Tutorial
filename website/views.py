from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from . import db
import json
import operator

views = Blueprint('views', __name__)

# f = open('styles.json')

# data = json.load(f)
@views.route('/', methods=['GET', 'POST'])
@views.route('/question', methods=['GET', 'POST'])
def home():
    #if request.method == 'POST': 
    #     note = request.form.get('note')#Gets the note from the HTML 

    #     if len(note) < 1:
    #         flash('Note is too short!', category='error') 
    #     else:
    #         new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
    #         db.session.add(new_note) #adding the note to the database 
    #         db.session.commit()
    #         flash('Note added!', category='success')
    

    ##return redirect(url_for('views.answer'))
    return render_template("question.html")

@views.route('/answer', methods=['POST'])
def answer():
    #Dictionary to hold scores, value is the index of the style in the json file
    stylesDict = {'Client-Server':{'Score':50, 'Value':0}, 'MPS':{'Score':50, 'Value':1}, 'PTP':{'Score':50, 'Value':2}, 'PipeAndFilter':{'Score':50, 'Value':3}, 'BatchSequential':{'Score':50, 'Value':4}, 'Blackboard':{'Score':50, 'Value':5}, 'Interpreter':{'Score':50, 'Value':6}, 'PubSub':{'Score':50, 'Value': 7}}

    data = request.form
    #Question 1
    if(int(data['Q1']) < 3):
        stylesDict['PipeAndFilter']['Score'] += 5
        stylesDict['MPS']['Score'] += 5
    else:
        stylesDict['MPS']['Score'] -= 5
        stylesDict['Blackboard']['Score'] -= 5
    #Question 2

    #Question 3
    if(int(data['Q3']) > 3):
        stylesDict['PTP']['Score'] -= 5
    
    #Question 4
    if(int(data['Q4']) > 3):
        stylesDict['PTP']['Score'] += 5
    
    #Question 5

    #Question 6
    if(int(data['Q6']) > 3):
        stylesDict['PTP']['Score'] += 5
        stylesDict['PipeAndFilter']['Score'] += 5
        stylesDict['Interpreter']['Score'] -= 5
        stylesDict['BatchSequential']['Score'] -= 5
    
    #Question 7
    if(int(data['Q7']) > 3):
        stylesDict['MPS']['Score'] -= 5
        stylesDict['PTP']['Score'] += 5
        stylesDict['PubSub']['Score'] += 5

    #Question 8
    if(int(data['Q8']) > 3):
        stylesDict['MPS']['Score'] -= 5
        stylesDict['PipeAndFilter']['Score'] += 5
        stylesDict['BatchSequential']['Score'] += 5

    #Question 9
    if(int(data['Q9']) > 3):
        stylesDict['Client-Server']['Score'] += 5
    else:
        stylesDict['PTP']['Score'] += 5
        stylesDict['Client-Server']['Score'] -= 5

    #Question 10
    if(int(data['Q10']) > 3):
        stylesDict['PTP']['Score'] += 5
        stylesDict['Interpreter']['Score'] += 5
        stylesDict['PipeAndFilter']['Score'] -= 5
        stylesDict['PubSub']['Score'] -= 5
        stylesDict['BatchSequential']['Score'] -= 5
    else:
        stylesDict['PipeAndFilter']['Score'] += 5
        stylesDict['BatchSequential']['Score'] += 5
        stylesDict['PubSub']['Score'] += 5

    #Question 11
    if(int(data['Q11']) > 3):
        stylesDict['Interpreter']['Score'] += 5
    else:
        stylesDict['Interpreter']['Score'] -= 5

    #Question 12
    if(int(data['Q12']) > 3):
        stylesDict['Client-Server']['Score'] -= 5
        stylesDict['PTP']['Score'] -= 5
        stylesDict['PubSub']['Score'] -= 5

    #Question 13
    if(int(data['Q13']) > 3):
        stylesDict['PipeAndFilter']['Score'] -= 5
        stylesDict['BatchSequential']['Score'] -= 5

    #Question 14
    if(int(data['Q14']) > 3):
        stylesDict['PipeAndFilter']['Score'] += 5
        stylesDict['BatchSequential']['Score'] += 5
    else:
        stylesDict['Interpreter']['Score'] += 5

    #Question 15
    if(int(data['Q15']) > 3):
        stylesDict['Client-Server']['Score'] += 5
        stylesDict['PTP']['Score'] += 5
    else:
        stylesDict['PTP']['Score'] -= 5
        stylesDict['PipeAndFilter']['Score'] -= 5

    #Question 16
    if(int(data['Q16']) > 3):
        stylesDict['PTP']['Score'] += 5
        stylesDict['PipeAndFilter']['Score'] -= 5
        stylesDict['BatchSequential']['Score'] -= 5
        stylesDict['PubSub']['Score'] -= 5
    else:
        stylesDict['Client-Server']['Score'] += 5
        stylesDict['PipeAndFilter']['Score'] += 5
        stylesDict['BatchSequential']['Score'] += 5
        stylesDict['PubSub']['Score'] += 5

    #Question 17
    if(int(data['Q17']) > 3):
        stylesDict['PTP']['Score'] += 5
    else:
        stylesDict['PTP']['Score'] -= 5
        stylesDict['PipeAndFilter']['Score'] += 5

    #Question 18
    if(int(data['Q18']) > 3):
        stylesDict['BatchSequential']['Score'] += 5
        stylesDict['Interpreter']['Score'] += 5
        stylesDict['MPS']['Score'] -= 5

    #Question 19
    if(int(data['Q19']) > 3):
        stylesDict['Client-Server']['Score'] -= 5
        stylesDict['PipeAndFilter']['Score'] += 5
    else:
        stylesDict['Client-Server']['Score'] += 5
        stylesDict['PipeAndFilter']['Score'] -= 5

    print(stylesDict)
    highScore = max(stylesDict, key=lambda v: stylesDict[v].get('Score', float('-inf')))

    f = open('C:\\Users\\kaden\\Desktop\\Software Architecture Project\\Software-Architecture-Optimization\website\\styles.json')
    styles = json.load(f)

    return render_template("answer.html", text = styles["styles"][stylesDict[highScore]['Value']])


# @views.route('/delete-note', methods=['POST'])
# def delete_note():  
#     note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
#     noteId = note['noteId']
#     note = Note.query.get(noteId)
#     if note:
#         if note.user_id == current_user.id:
#             db.session.delete(note)
#             db.session.commit()

#     return jsonify({})
