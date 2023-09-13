from flask import Blueprint, render_template, redirect, url_for, session, request, Response

from models.model import db, Booking, Exhibition
from decorators import check_user_login

booking_list_bp = Blueprint('booking_list', __name__)

@booking_list_bp.route('/user/booking_list')
@check_user_login
def booking_list():
    user_id = session["user_id"]
    booking = db.session.query(
        Booking.id,
        Exhibition.title,
        Booking.visited_at,
        Booking.ticket_type) \
        .filter(Booking.user_id==user_id) \
        .join(Exhibition, Exhibition.id == Booking.exhibition_id) \
        .order_by(Booking.visited_at.desc()) \
        .all()
    
    result = {}
    result['booking'] = [{
        'booking_id': row.id,
        'exhibition_title': row.title,
        'visited_at': row.visited_at.date(),
        'ticket_type': row.ticket_type.value
    } for row in booking]
 
    return render_template('user/booking_list.html', data=result)