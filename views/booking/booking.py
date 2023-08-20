from flask import Blueprint, render_template


booking_bp = Blueprint('booking', __name__)

@booking_bp.route('/booking')
def booking():
    return "<h1>hi</h1>"

@booking_bp.route('/booking/exhibition/<id>')
def booking_detail(id):
    return "<h1>hi exhibition booking</h1>"