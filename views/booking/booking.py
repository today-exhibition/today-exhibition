from flask import Blueprint, render_template, session, request
from datetime import datetime, timedelta
from sqlalchemy import and_
from utils import load_secrets
import base64
import json
import requests

from models.model import db, Exhibition, TicketPrice, Gallery, LikeExhibition, User
from views.search.search_exhibition import calc_pages
from views.exhibition.exhibition import get_exhibition_data
from decorators import check_user_login


booking_bp = Blueprint('booking', __name__)

#! TODO: ticket_price 없으면 0원으로 진행
#! TODO: 나중에 데이터 추가 후 예외처리 추가하기

# 2023.09.09 수정
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
    
    exhibition = get_exhibition_data(id)
    exhibition = [row._asdict() for row in exhibition][0]

    data =  {
        "user": user,
        "working": True,
        "exhibition": exhibition
    }
    
    return render_template('booking/booking.html', data=data)

@booking_bp.route('/booking/success', methods=['GET'])
def booking_success():
    order_id = request.args.get('orderId')
    amount = request.args.get('amount')
    payment_key = request.args.get('paymentKey')

    url = "https://api.tosspayments.com/v1/payments/confirm"

    secrets = load_secrets()
    payments_keys = secrets.get("payments")

    secretKey = payments_keys.get("toss_payments_secret")
    userpass = secretKey + ':'
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
    
    # final_price = price, quantity

    data = {
        "res" : pretty,
        "respaymentKey" : respaymentKey,
        "resorderId" : resorderId,
        }
    return render_template("booking/success.html", data=data)