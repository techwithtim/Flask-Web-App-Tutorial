from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from . import db
import json

views = Blueprint('views', __name__)

# f = open('styles.json')

# data = json.load(f)

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
    

    if request.method == 'POST':
        return redirect(url_for('views.answer'))
    return render_template("question.html")

@views.route('/answer')
def answer():
    return render_template("answer.html")


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
