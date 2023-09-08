from flask import Blueprint, request, render_template, session
from sqlalchemy import func, case, Cast, String

from models.model import ArtistExhibition, db, Exhibition, Gallery, GalleryAddress, LikeExhibition, FollowingGallery, Artist, FollowingArtist

search_bp = Blueprint('search', __name__)

@search_bp.route('/search')
def search():
    keyword = request.args.get('keyword', default="", type=str).strip()
    user_id = session.get('user_id', None)

    exhibitions = get_exhibitions(user_id, keyword) \
        .join(GalleryAddress, Gallery.id == GalleryAddress.gallery_id, isouter=True) \
        .all()
    artists = get_artists(user_id, keyword).all()    
    galleries = get_galleries(user_id, keyword).all()

    # 각 데이터 검색 결과 개수
    exhibition_count = len(exhibitions)
    gallery_count = len(galleries)
    artist_count = len(artists)

    data = {
        "exhibitions": [row._asdict() for row in exhibitions][:3],
        "galleries": [row._asdict() for row in galleries][:5],
        "artists": [row._asdict() for row in artists][:5],
        "exhibition_count": exhibition_count,
        "gallery_count": gallery_count,
        "artist_count": artist_count,
        "keyword": keyword
    }

    return render_template('search/search.html', data=data)

def get_exhibitions(user_id, keyword):
    liked_subquery = db.session.query(
        LikeExhibition.exhibition_id,
        func.count('*').label('likes')) \
        .filter(LikeExhibition.user_id == user_id) \
        .group_by(LikeExhibition.exhibition_id) \
        .subquery()

    query = db.session.query(
        Exhibition.id.label('exhibition_id'),
        Exhibition.title.label("exhibition_title"),
        Exhibition.thumbnail_img,
        Cast(Exhibition.start_date, String).label('start_date'),
        Cast(Exhibition.end_date, String).label('end_date'),
        Gallery.name.label("gallery_name"),
        case(
            (liked_subquery.c.likes, 1),
            else_=0).label('liked')) \
        .filter(Exhibition.title.like('%' + keyword + '%')) \
        .join(Gallery, Gallery.id == Exhibition.gallery_id) \
        .outerjoin(liked_subquery, liked_subquery.c.exhibition_id == Exhibition.id) \
        .order_by(Exhibition.start_date.desc())          
                
    return query

def get_artists(user_id, keyword):
    followed_subquery = db.session.query(
        FollowingArtist.artist_id,
        func.count('*').label('follows')) \
        .filter(FollowingArtist.user_id == user_id) \
        .group_by(FollowingArtist.artist_id) \
        .subquery()
    
    query = db.session.query(
        Artist.id,
        Artist.name,
        Artist.thumbnail_img.label('artist_thumbnail_img'),
        Exhibition.thumbnail_img.label('exhibition_thumbnail_img'),
        case(
            (followed_subquery.c.follows, 1),
            else_=0).label('followed')) \
        .filter(Artist.name.like('%' + keyword + '%')) \
        .outerjoin(followed_subquery, followed_subquery.c.artist_id == Artist.id) \
        .join(ArtistExhibition, Artist.id == ArtistExhibition.artist_id) \
        .join(Exhibition, ArtistExhibition.exhibition_id == Exhibition.id) \
        .group_by(Artist.id) \
        .order_by(Artist.id)
    
    return query

def get_galleries(user_id, keyword):
    followed_subquery = db.session.query(
        FollowingGallery.gallery_id,
        func.count('*').label('follows')) \
        .filter(FollowingGallery.user_id == user_id) \
        .group_by(FollowingGallery.gallery_id) \
        .subquery()
    
    query = db.session.query(
        Gallery.id,
        Gallery.name,
        Gallery.thumbnail_img.label('gallery_thumbnail_img'),
        Exhibition.thumbnail_img.label('exhibition_thumbnail_img'),
        case(
            (followed_subquery.c.follows, 1),
            else_=0).label('followed')) \
        .filter(Gallery.name.like('%' + keyword + '%')) \
        .outerjoin(followed_subquery, followed_subquery.c.gallery_id == Gallery.id) \
        .join(Exhibition, Gallery.id == Exhibition.gallery_id) \
        .group_by(Gallery.id) \
        .order_by(Gallery.id)
    
    return query

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

