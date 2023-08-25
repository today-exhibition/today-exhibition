from flask import Blueprint, request, render_template, session
from sqlalchemy import desc

from models.model import db, Exhibition, Gallery, GalleryAddress, LikeExhibition, FollowingGallery, Artist, FollowingArtist

search_bp = Blueprint('search', __name__)

@search_bp.route('/search')
def search():
    keyword = request.args.get('keyword', default="", type=str).strip()
    user_id = session.get('user_id', None)

    exhibitions = get_search_exhibitions(keyword) \
        .join(GalleryAddress, Gallery.id == GalleryAddress.gallery_id, isouter=True) \
        .all()
    artists = get_search_artists(keyword).all()    
    gallerys = get_search_gallerys(keyword).all()

    # 각 데이터 검색 결과 개수
    exhibition_count = len(exhibitions)
    gallery_count = len(gallerys)
    artist_count = len(artists)

    # 사용자가 좋아요, 팔로우한 id 목록
    liked_exhibition_ids = get_liked_exhibition_ids(user_id)
    followed_gallery_ids = get_followed_gallery_ids(user_id)
    followed_artist_ids = get_followed_artist_ids(user_id)

    data = {
        "exhibition_list": exhibitions[:3],
        "gallery_list": gallerys[:3],
        "artist_list": artists[:3],
        "exhibition_count": exhibition_count,
        "gallery_count": gallery_count,
        "artist_count": artist_count,
        "liked_exhibition_ids": liked_exhibition_ids,
        "followed_gallery_ids": followed_gallery_ids,
        "followed_artist_ids": followed_artist_ids,
        "keyword": keyword,
        "user_id": user_id
    }

    return render_template('search/search.html', data=data)

def get_search_exhibitions(keyword):
    exhibitions_query = db.session.query(
        Exhibition.id,
        Exhibition.title,
        Exhibition.start_date,
        Exhibition.end_date,
        Gallery.name,
        Exhibition.thumbnail_img
        ) \
        .filter(Exhibition.title.like('%' + keyword + '%')) \
        .join(Gallery, Exhibition.gallery_id == Gallery.id) \
        .order_by(desc(Exhibition.start_date)) 
    
    return exhibitions_query

def get_search_artists(keyword):
    artists_query = db.session.query(
        Artist.id,
        Artist.name,
        Artist.thumbnail_img
        ) \
        .filter(Artist.name.like('%' + keyword + '%')) \
        .order_by(Artist.id) 

    return artists_query

def get_search_gallerys(keyword):
    gallerys_query = db.session.query(
        Gallery.id,
        Gallery.name,
        Gallery.thumbnail_img,
        ) \
        .filter(Gallery.name.like('%' + keyword + '%')) \
        .order_by(Gallery.id)
    
    return gallerys_query

def get_liked_exhibition_ids(user_id):
    if user_id:
        return [like.exhibition_id for like in LikeExhibition.query.filter_by(user_id=user_id).all()]
    return []

def get_followed_gallery_ids(user_id):
    if user_id:
        return [follow.gallery_id for follow in FollowingGallery.query.filter_by(user_id=user_id).all()]
    return []

def get_followed_artist_ids(user_id):
    if user_id:
        return [follow.artist_id for follow in FollowingArtist.query.filter_by(user_id=user_id).all()]
    return []

