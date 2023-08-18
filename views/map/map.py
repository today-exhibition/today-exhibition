import json
import datetime
from flask import Blueprint, render_template
from sqlalchemy import func

from models.model import db, Exhibition, Gallery, GalleryAddress, LikeExhibition

map_bp = Blueprint('map', __name__)

@map_bp.route('/map/')
def map() :
    with open("secrets.json", "r") as secrets_file:
        secrets = json.load(secrets_file)
    kakao_map_api_key = secrets["map"]["kakao_api_key"]

    map_list = db.session.query(Exhibition.id.label("exhibition_id"), Exhibition.title.label("exhibition_title"), Exhibition.thumbnail_img, Exhibition.start_date, Exhibition.end_date, Gallery.name.label("gallery_name"), GalleryAddress.gpsx, GalleryAddress.gpsy) \
      .join(Gallery, Gallery.id == Exhibition.gallery_id) \
      .join(GalleryAddress, Gallery.id == GalleryAddress.gallery_id) \
      .all()
    
    result_list = []
    for item in map_list:
        result_list.append({
            "exhibition_id": item.exhibition_id,
            "exhibition_title": item.exhibition_title,
            "thumbnail_img": item.thumbnail_img,
            "start_date": str(item.start_date),
            "end_date": str(item.end_date),
            "gallery_name": item.gallery_name,
            "gpsx": item.gpsx,
            "gpsy": item.gpsy
        })
    exhibition_list = json.dumps(result_list, ensure_ascii=False)
    return render_template("map/map.html", api_key=kakao_map_api_key, exhibition_list=exhibition_list, type="exhibition")

#! [곧 종료되는 전시 : 2주 이내에 종료되는 전시]
@map_bp.route('/map/ending_soon')
def ending_soon():
    with open("secrets.json", "r") as secrets_file:
        secrets = json.load(secrets_file)
    kakao_map_api_key = secrets["map"]["kakao_api_key"]

    map_list = db.session.query(Exhibition.id.label("exhibition_id"), Exhibition.title.label("exhibition_title"), Exhibition.thumbnail_img, Exhibition.start_date, Exhibition.end_date, Gallery.name.label("gallery_name"), GalleryAddress.gpsx, GalleryAddress.gpsy) \
      .join(Gallery, Gallery.id == Exhibition.gallery_id) \
      .join(GalleryAddress, Gallery.id == GalleryAddress.gallery_id) \
      .filter(Exhibition.end_date < datetime.datetime.today() + datetime.timedelta(weeks = 2)) \
      .all()
    
    result_list = []
    for item in map_list:
        result_list.append({
            "exhibition_id": item.exhibition_id,
            "exhibition_title": item.exhibition_title,
            "thumbnail_img": item.thumbnail_img,
            "start_date": str(item.start_date),
            "end_date": str(item.end_date),
            "gallery_name": item.gallery_name,
            "gpsx": item.gpsx,
            "gpsy": item.gpsy
        })
    exhibition_list = json.dumps(result_list, ensure_ascii=False)
    return render_template("map/map.html", api_key=kakao_map_api_key, exhibition_list=exhibition_list, type="ending_soon")

#! [지금 주목받는 전시 : 최근 1주 하트 많이 찍힌 전시]
@map_bp.route('/map/featured')
def featured():
    pass

#! [인기순 : 전체 하트순 전시]
@map_bp.route('/map/popular')
def popular():
    with open("secrets.json", "r") as secrets_file:
        secrets = json.load(secrets_file)
    kakao_map_api_key = secrets["map"]["kakao_api_key"]

    map_list = db.session.query(func.count('*'), Exhibition.id.label("exhibition_id"), Exhibition.title.label("exhibition_title"), Exhibition.thumbnail_img, Exhibition.start_date, Exhibition.end_date, Gallery.name.label("gallery_name"), GalleryAddress.gpsx, GalleryAddress.gpsy) \
      .join(Gallery, Gallery.id == Exhibition.gallery_id) \
      .join(GalleryAddress, Gallery.id == GalleryAddress.gallery_id) \
      .join(LikeExhibition, LikeExhibition.exhibition_id == Exhibition.id) \
      .group_by(LikeExhibition.exhibition_id) \
      .order_by(func.count('*').desc()) \
      .all()
    
    result_list = []
    for item in map_list:
        result_list.append({
            "exhibition_id": item.exhibition_id,
            "exhibition_title": item.exhibition_title,
            "thumbnail_img": item.thumbnail_img,
            "start_date": str(item.start_date),
            "end_date": str(item.end_date),
            "gallery_name": item.gallery_name,
            "gpsx": item.gpsx,
            "gpsy": item.gpsy
        })
    exhibition_list = json.dumps(result_list, ensure_ascii=False)
    return render_template("map/map.html", api_key=kakao_map_api_key, exhibition_list=exhibition_list, type="popular")

#! [추천 전시 : 큐레이팅 전시]
@map_bp.route('/map/recommended')
def recommended():
    pass