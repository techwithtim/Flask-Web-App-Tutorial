from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import WeightEntry
from . import db
from datetime import datetime as dt

weight_tracker_bp = Blueprint('weight_tracker', __name__)

@weight_tracker_bp.route('/weight-tracker', methods=['GET', 'POST'])
@login_required
def weight_tracker():
    if request.method == 'POST':
        weight = float(request.form.get('weight'))
        new_weight_entry = WeightEntry(user_id=current_user.id, weight=weight)
        db.session.add(new_weight_entry)
        db.session.commit()
        flash('Weight added successfully!', category='success')
        return redirect(url_for('weight_tracker.weight_tracker'))

    return render_template('weight_tracker.html')

# Add routes for editing and deleting weight entries if needed

# Example model definition for WeightEntry
