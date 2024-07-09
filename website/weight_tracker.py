from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from .models import WeightEntry
from . import db

weight_tracker_bp = Blueprint('weight_tracker', __name__)

@weight_tracker_bp.route('/weight_tracker', methods=['GET', 'POST'])
@login_required
def weight_tracker():
    if request.method == 'POST':
        weight = request.form.get('weight')
        if weight:
            new_weight_entry = WeightEntry(weight=float(weight), user_id=current_user.id)
            db.session.add(new_weight_entry)
            db.session.commit()
            flash('Weight entry added!', category='success')
        else:
            flash('Please enter a valid weight.', category='error')
    weight_entries = WeightEntry.query.filter_by(user_id=current_user.id).order_by(WeightEntry.date).all()
    return render_template('weight_tracker.html', user=current_user, weight_entries=weight_entries)

@weight_tracker_bp.route('/get_weights')
@login_required
def get_weights():
    weight_entries = WeightEntry.query.filter_by(user_id=current_user.id).order_by(WeightEntry.date).all()
    weights_data = [{"date": we.date.strftime("%Y-%m-%d"), "weight": we.weight} for we in weight_entries]
    return jsonify(weights_data)
