import json
from flask import Blueprint, render_template

from models.model import db, Exhibition, Gallery, GalleryAddress

map_bp = Blueprint('map', __name__)

@map_bp.route('/map/')
def map() :
    with open("secrets.json", "r") as secrets_file:
        secrets = json.load(secrets_file)
    kakao_map_api_key = secrets["api"]["kakao_api_key"]

    map_list = db.session.query(Exhibition.title.label("exhibition_title"), Exhibition.thumbnail_img, Exhibition.start_date, Exhibition.end_date, Gallery.name.label("gallery_name"), GalleryAddress.gpsx, GalleryAddress.gpsy) \
      .join(Gallery, Gallery.id == Exhibition.gallery_id) \
      .join(GalleryAddress, Gallery.id == GalleryAddress.gallery_id) \
      .all()
    
    result_list = []
    for item in map_list:
        result_list.append({
            "exhibition_title": item.exhibition_title,
            "thumbnail_img": item.thumbnail_img,
            "start_date": str(item.start_date),
            "end_date": str(item.end_date),
            "gallery_name": item.gallery_name,
            "gpsx": item.gpsx,
            "gpsy": item.gpsy
        })
    exhibition_list = json.dumps(result_list, ensure_ascii=False)
    return render_template("map.html", api_key=kakao_map_api_key, exhibition_list=exhibition_list)