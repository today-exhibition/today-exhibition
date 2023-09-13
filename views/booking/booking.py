from flask import Blueprint, render_template, session, request
from datetime import datetime
from utils import load_secrets
import base64
import json
import requests

from models.model import Booking, db, TicketPrice, User
from views.exhibition.exhibition import get_exhibition_data
from decorators import check_user_login


booking_bp = Blueprint('booking', __name__)

#! TODO: ticket_price 없으면 0원으로 진행
#! TODO: 나중에 데이터 추가 후 예외처리 추가하기

@booking_bp.route('/booking/exhibition/<id>', methods=['GET'])
@check_user_login
def booking_detail(id):
    user_id = session.get('user_id')
    user = db.session.query(
        User.id,
        User.email,
        User.nickname) \
        .filter(User.id == user_id) \
        .all()
    user = [row._asdict() for row in user][0]

    current_date = datetime.now().date()
    
    exhibition = get_exhibition_data(id)
    exhibition = [row._asdict() for row in exhibition][0]
    
    exhibition_price = db.session.query(
        TicketPrice.ticket_type,
        TicketPrice.final_price)\
        .filter(TicketPrice.exhibition_id == id) \
        .order_by(TicketPrice.final_price.desc()) \
        .all()
    exhibition_price = [{
        'ticket_type': row.ticket_type.value,
        'ticket_type_name': row.ticket_type.name,
        'final_price': row.final_price
    } for row in exhibition_price]

    data =  {
        "user": user,
        "current_date": current_date,
        "working": True,
        "exhibition": exhibition,
        "exhibition_price" : exhibition_price
    }
    
    return render_template('booking/booking.html', data=data)

@booking_bp.route('/booking/success/<date>/<exhibition_id>/<type>', methods=['GET'])
def booking_success(date, exhibition_id, type):
    user_id = session.get('user_id')
    date = datetime.strptime(date, '%Y-%m-%d').date()
    
    order_id = request.args.get('orderId')
    amount = request.args.get('amount')
    payment_key = request.args.get('paymentKey')

    url = "https://api.tosspayments.com/v1/payments/confirm"

    secrets = load_secrets()
    userpass = secrets['payments']['toss_payments_secret'] + ':'
    encoded_u = base64.b64encode(userpass.encode()).decode()

    headers = {
        "Authorization" : "Basic %s" % encoded_u,
        "Content-Type": "application/json"
    }
    
    params = {
        "orderId" : order_id,
        "amount" : amount,
        "paymentKey": payment_key,
    }
    
    res = requests.post(url, data=json.dumps(params), headers=headers)
    resjson = res.json()
    pretty = json.dumps(resjson, indent=4)

    respaymentKey = resjson["paymentKey"]
    resorderId = resjson["orderId"]

    data = {
        "res" : pretty,
        "respaymentKey" : respaymentKey,
        "resorderId" : resorderId,
        }
    
    new_booking = Booking(id=order_id, user_id=user_id, exhibition_id=exhibition_id, visited_at=date, ticket_type=type)
    db.session.add(new_booking)
    db.session.commit()

    return render_template("booking/success.html", data=data)