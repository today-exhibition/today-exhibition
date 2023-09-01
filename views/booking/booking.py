from flask import Blueprint, render_template, session, request
from flask import redirect, url_for
from datetime import datetime
from sqlalchemy import and_
from utils import load_secrets

from models.model import db, Exhibition, TicketPrice, Gallery, LikeExhibition
from views.search.search_exhibition import calc_pages
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
@booking_bp.route('/booking/exhibition/<id>', methods=['GET'])
@check_user_login
def booking_detail(id):
    current_date = datetime.now().date()
    
    info_exhibition = db.session.query(
                            Exhibition.id,
                            Exhibition.title,
                            Exhibition.start_date,
                            Exhibition.end_date,
                            Gallery.name,
                            Exhibition.thumbnail_img,
                            TicketPrice.final_price
                        ) \
                        .filter(Exhibition.id == id) \
                        .join(Gallery, Exhibition.gallery_id == Gallery.id) \
                        .outerjoin(TicketPrice, Exhibition.id == TicketPrice.exhibition_id) \
                        .first()
                    
    info_dict = {
        "id": info_exhibition.id,
        "title": info_exhibition.title,
        "start_date": info_exhibition.start_date,
        "end_date": info_exhibition.end_date,
        "gallery_name": info_exhibition.name,
        "thumbnail_img": info_exhibition.thumbnail_img,
        "ticket_price": info_exhibition.final_price or 10  # final_price가 None인 경우 0
    }
        
    return render_template('booking/booking.html', id=id, working=True,
                           exhibition=info_dict, current_date=current_date, info_dict=info_dict)
    
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