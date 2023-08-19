import json
import datetime
from flask import Blueprint, render_template, session
from sqlalchemy import func, case



from models.model import db, Exhibition, Gallery, GalleryAddress, LikeExhibition


map_bp = Blueprint('map', __name__)

def load_kakao_map_api():
    with open("secrets.json", "r") as secrets_file:
        secrets = json.load(secrets_file)
    kakao_map_api_key = secrets["map"]["kakao_api_key"]
    return kakao_map_api_key

def convert_rowlist_to_json(row_list):
    result = []
    for item in row_list:
        result.append({
            "exhibition_id": item.exhibition_id,
            "exhibition_title": item.exhibition_title,
            "thumbnail_img": item.thumbnail_img,
            "start_date": str(item.start_date),
            "end_date": str(item.end_date),
            "gallery_name": item.gallery_name,
            "gpsx": item.gpsx,
            "gpsy": item.gpsy,
            "liked" : item.likes
        })
    result = json.dumps(result, ensure_ascii=False)
    return result

def get_exhibition_list(user_id, session, filter_type=None):
    liked_subquery = session.query(
        LikeExhibition.exhibition_id,
        func.count('*').label('liked')) \
        .filter(LikeExhibition.user_id == user_id) \
        .group_by(LikeExhibition.exhibition_id) \
        .subquery('S')

    query = session.query(
            Exhibition.id.label('exhibition_id'),
            Exhibition.title.label("exhibition_title"),
            Exhibition.thumbnail_img,
            Exhibition.start_date,
            Exhibition.end_date,
            Gallery.name.label("gallery_name"),
            GalleryAddress.gpsx,
            GalleryAddress.gpsy,
            case(
                (liked_subquery.c.liked, 1),
                else_=0).label('likes')) \
            .join(Gallery, Gallery.id == Exhibition.gallery_id) \
            .join(GalleryAddress, Gallery.id == GalleryAddress.gallery_id) \
            .outerjoin(liked_subquery, liked_subquery.c.exhibition_id == Exhibition.id)

    if filter_type == 'ending_soon':
        query = query.filter(Exhibition.end_date < datetime.datetime.today() + datetime.timedelta(weeks=2))
    elif filter_type == 'featured':
        query = query.filter(LikeExhibition.liked_at > datetime.datetime.today() - datetime.timedelta(weeks=1)) \
            .group_by(LikeExhibition.exhibition_id) \
            .order_by(func.count('*').desc())
    elif filter_type == 'popular':
        query = query.group_by(LikeExhibition.exhibition_id) \
            .order_by(func.count('*').desc()) \
                
    return query.all()

@map_bp.route('/map/')
def map() :
    user_id = session["user_id"]
    kakao_map_api_key = load_kakao_map_api()
    exhibition_list = get_exhibition_list(user_id, db.session)
    print(exhibition_list)
    exhibition_list = convert_rowlist_to_json(exhibition_list)
    return render_template("map/map.html", api_key=kakao_map_api_key, exhibition_list=exhibition_list, type="exhibition")

#! [곧 종료되는 전시 : 2주 이내에 종료되는 전시]
@map_bp.route('/map/ending_soon')
def ending_soon():
    user_id = session["user_id"]
    kakao_map_api_key = load_kakao_map_api()
    exhibition_list = get_exhibition_list(user_id, db.session, 'ending_soon')
    exhibition_list = convert_rowlist_to_json(exhibition_list)
    return render_template("map/map.html", api_key=kakao_map_api_key, exhibition_list=exhibition_list, type="ending_soon")

#! [지금 주목받는 전시 : 최근 1주 하트 많이 찍힌 전시]
@map_bp.route('/map/featured')
def featured():
    user_id = session["user_id"]
    kakao_map_api_key = load_kakao_map_api()
    exhibition_list = get_exhibition_list(user_id, db.session, 'featured')
    exhibition_list = convert_rowlist_to_json(exhibition_list)
    return render_template("map/map.html", api_key=kakao_map_api_key, exhibition_list=exhibition_list, type="featured")

#! [인기순 : 전체 하트순 전시]
@map_bp.route('/map/popular')
def popular():
    user_id = session["user_id"]
    kakao_map_api_key = load_kakao_map_api()
    exhibition_list = get_exhibition_list(user_id, db.session, 'popular')    
    exhibition_list = convert_rowlist_to_json(exhibition_list)
    return render_template("map/map.html", api_key=kakao_map_api_key, exhibition_list=exhibition_list, type="popular")

#! [추천 전시 : 큐레이팅 전시]
@map_bp.route('/map/recommended')
def recommended():
    pass