from flask import Blueprint, render_template, session, request
from flask import redirect, url_for
from datetime import datetime, timedelta
from sqlalchemy import and_
from utils import load_secrets

from models.model import db, Exhibition, TicketPrice, Gallery, LikeExhibition
from views.search.search_exhibition import calc_pages
from views.exhibition.exhibition import get_exhibition_data
from decorators import check_user_login


booking_bp = Blueprint('booking', __name__)

@booking_bp.route('/booking')
@check_user_login
def booking():
    page = request.args.get('page', default=1, type=int)
    current_date = datetime.now().date()
    
    user_id = session.get('user_id', None)
    available_exhibitions = db.session.query(
                                Exhibition.id,
                                Exhibition.title,
                                Exhibition.start_date,
                                Exhibition.end_date,
                                Gallery.name,
                                Exhibition.thumbnail_img
                            ) \
                            .filter(and_(Exhibition.start_date <= current_date, Exhibition.end_date >= current_date)) \
                            .join(Gallery, Exhibition.gallery_id == Gallery.id) \
                            .all()
    
    exhibition_count = len(available_exhibitions)
    total_pages, current_page, page_data, page_list = calc_pages(available_exhibitions, page)
    
    liked_exhibition_ids = []  
    if user_id:
        liked_exhibition_ids = [like.exhibition_id for like in LikeExhibition.query.filter_by(user_id=user_id).all()]

    return render_template('search/search_exhibition.html', 
                           exhibitions=page_data, exhibition_count=exhibition_count, liked_exhibition_ids=liked_exhibition_ids, 
                           total_pages=total_pages, current_page=current_page, page_list=page_list)

#! TODO: ticket_price 없으면 0원으로 진행
#! TODO: 나중에 데이터 추가 후 예외처리 추가하기

# 2023.09.09 수정
@booking_bp.route('/booking/exhibition/<id>', methods=['GET'])
@check_user_login
def booking_detail(id):
    exhibition = get_exhibition_data(id)
    # 전시일자 리스트
    date_range = []
    current_date = datetime.now().date()  
    while current_date <= exhibition.end_date:
        date_range.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=1)
    data =  {
    "id": id,
    "working": True,
    "exhibition": exhibition,
    "date_range": date_range
    }
    return render_template('booking/booking.html', data=data)

@booking_bp.route('/booking/booking_success', methods=['POST'])
@check_user_login
def booking_success():
    price = int(request.form.get('price'))
    quantity = request.form.get('quantity')
    print(price, quantity)
    
    secrets = load_secrets()
    payments_keys = secrets.get("payments")
    payments_keys.get("toss_payments_id")
    payments_keys.get("toss_payments_secret")
    
    user_id = session.get('user_id')
    final_price = price, quantity
    return ""