import datetime
from flask import Blueprint, render_template, session
from sqlalchemy import false, func, case, and_, Cast, String

from models.model import db, Exhibition, Gallery, GalleryAddress, LikeExhibition


map_bp = Blueprint('map', __name__)

def convert_rowlist_to_json(type, row_list):
    result = {}
    result['type'] = type
    result['data'] = [row._asdict() for row in row_list]
    
    return result

def get_exhibition_list(user_id, session, filter_type=None):
    liked_subquery = session.query(
        LikeExhibition.exhibition_id,
        func.count('*').label('likes')) \
        .filter(LikeExhibition.user_id == user_id) \
        .group_by(LikeExhibition.exhibition_id) \
        .subquery()

    query = session.query(
        Exhibition.id.label('exhibition_id'),
        Exhibition.title.label("exhibition_title"),
        Exhibition.thumbnail_img,
        Cast(Exhibition.start_date, String).label('start_date'),
        Cast(Exhibition.end_date, String).label('end_date'),
        Gallery.name.label("gallery_name"),
        GalleryAddress.gpsx,
        GalleryAddress.gpsy,
        case(
            (liked_subquery.c.likes, 1),
            else_=0).label('liked')) \
        .join(Gallery, Gallery.id == Exhibition.gallery_id) \
        .join(GalleryAddress, Gallery.id == GalleryAddress.gallery_id) \
        .outerjoin(liked_subquery, liked_subquery.c.exhibition_id == Exhibition.id)

    if filter_type == 'ending_soon':
        query = query.filter(and_(Exhibition.end_date < datetime.datetime.today() + datetime.timedelta(weeks=2), datetime.datetime.today() < Exhibition.end_date)) \
            .order_by(Exhibition.end_date.asc())
    elif filter_type == 'featured':
        query = query.join(LikeExhibition, LikeExhibition.exhibition_id == Exhibition.id) \
            .filter(LikeExhibition.liked_at > datetime.datetime.today() - datetime.timedelta(weeks=1)) \
            .group_by(LikeExhibition.exhibition_id) \
            .order_by(func.count('*').desc())
    elif filter_type == 'popular':
        query = query.join(LikeExhibition, LikeExhibition.exhibition_id == Exhibition.id) \
            .group_by(LikeExhibition.exhibition_id) \
            .order_by(func.count('*').desc())
    elif filter_type == 'recommended' :
        query = query.filter(false())
                
    return query.all()

@map_bp.route('/map/')
def map() :
    user_id = session.get("user_id", None)
    exhibition_list = get_exhibition_list(user_id, db.session)
    exhibition_list = convert_rowlist_to_json("exhibition", exhibition_list)

    return render_template("map/map.html", exhibition_list=exhibition_list)

#! [곧 종료되는 전시 : 2주 이내에 종료되는 전시]
@map_bp.route('/map/ending_soon')
def ending_soon():
    user_id = session.get("user_id", None)
    exhibition_list = get_exhibition_list(user_id, db.session, 'ending_soon')
    exhibition_list = convert_rowlist_to_json("ending_soon", exhibition_list)

    return render_template("map/map.html", exhibition_list=exhibition_list)

#! [지금 주목받는 전시 : 최근 1주 하트 많이 찍힌 전시]
@map_bp.route('/map/featured')
def featured():
    user_id = session.get("user_id", None)
    exhibition_list = get_exhibition_list(user_id, db.session, 'featured')
    exhibition_list = convert_rowlist_to_json("featured", exhibition_list)
    
    return render_template("map/map.html", exhibition_list=exhibition_list)

#! [인기순 : 전체 하트순 전시]
@map_bp.route('/map/popular')
def popular():
    user_id = session.get("user_id", None)
    exhibition_list = get_exhibition_list(user_id, db.session, 'popular')    
    exhibition_list = convert_rowlist_to_json("popular", exhibition_list)
    
    return render_template("map/map.html", exhibition_list=exhibition_list)

#! [추천 전시 : 큐레이팅 전시]
@map_bp.route('/map/recommended')
def recommended():
    user_id = session.get("user_id", None)
    exhibition_list = get_exhibition_list(user_id, db.session, 'recommended')    
    exhibition_list = convert_rowlist_to_json("recommended", exhibition_list)
    
    return render_template("map/map.html", exhibition_list=exhibition_list)