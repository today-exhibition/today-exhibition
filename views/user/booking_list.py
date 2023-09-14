from flask import Blueprint, render_template, session

from models.model import db, Booking, Exhibition, Billing
from decorators import check_user_login

booking_list_bp = Blueprint('booking_list', __name__)

@booking_list_bp.route('/user/booking_list')
@check_user_login
def booking_list():
    user_id = session["user_id"]
    booking = db.session.query(
        Booking.id,
        Exhibition.id.label('exhibition_id'),
        Exhibition.title,
        Booking.visited_at,
        Booking.ticket_type,
        Billing.requested_at,
        Billing.approved_at,
        Billing.billing_method,
        Billing.billing_status) \
        .filter(Booking.user_id==user_id) \
        .join(Exhibition, Exhibition.id == Booking.exhibition_id) \
        .join(Billing, Billing.booking_id == Booking.id) \
        .order_by(Booking.visited_at.asc()) \
        .all()
    
    result = {}
    result['booking'] = [{
        'booking_id': row.id,
        'exhibition_id': row.exhibition_id,
        'exhibition_title': row.title,
        'visited_at': row.visited_at.date(),
        'ticket_type': row.ticket_type.value,
        'billing_status': row.billing_status.name,
        'billing_method': row.billing_method.name
    } for row in booking]
 
    return render_template('user/booking_list.html', data=result)