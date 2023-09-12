from flask import Blueprint, render_template, redirect, url_for, session, request, Response

from models.model import db, Booking
from decorators import check_user_login

booking_list_bp = Blueprint('booking_list', __name__)

@booking_list_bp.route('/user/booking_list')
@check_user_login
def booking_list():
    user_id = session["user_id"]
    
    result = {}
 
    return render_template('user/booking_list.html', data=result)