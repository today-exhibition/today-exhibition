from flask import Blueprint, render_template, session
from sqlalchemy import Cast, String, case, func
from datetime import datetime
from models.model import db, Artist, Exhibition, Gallery, ArtistExhibition, FollowingArtist, LikeExhibition
from views.search.search import get_followed_artist_ids, get_liked_exhibition_ids
import uuid

artist_bp = Blueprint('artist', __name__)

# 작가 디테일(작가명, 전시상태, 작가팔로우, 전시좋아요)
@artist_bp.route('/artist/<id>')
def artist(id):
    user_id = session.get('user_id', None)
    artist = get_artist_data(id)\
        .filter(Artist.id == id)\
        .first()    
    exhibitions = get_exhibition_data(user_id)\
        .join(ArtistExhibition, ArtistExhibition.exhibition_id == Exhibition.id)\
        .join(Artist, Artist.id == ArtistExhibition.artist_id)\
        .filter(Artist.id == id)\
        .all()    
    # exhibition_status = get_exhibition_status(exhibitions)   
    
    followed_artist_ids = get_followed_artist_ids(user_id)
    liked_exhibition_ids = get_liked_exhibition_ids(user_id)

    data = {
        "artist": [artist._asdict()],
        "exhibitions": [row._asdict() for row in exhibitions],
        # "exhibition_status": exhibition_status,
        "user_id": user_id,
        "followed_artist_ids": followed_artist_ids,
        "liked_exhibition_ids": liked_exhibition_ids
        }

    return render_template('artist/artist.html', data=data)

# [함수] 작가 정보
def get_artist_data(id):
    artist = db.session.query(
        Artist.name,
        Artist.id)
            
    return artist
    
# [함수] 전시 정보
def get_exhibition_data(user_id):
    liked_subquery = db.session.query(
        LikeExhibition.exhibition_id,
        func.count('*').label('likes')) \
        .filter(LikeExhibition.user_id == user_id) \
        .group_by(LikeExhibition.exhibition_id) \
        .subquery()

    exhibitions = db.session.query(
        Exhibition.id.label('exhibition_id'),
        Exhibition.title.label("exhibition_title"),
        Exhibition.thumbnail_img,
        Cast(Exhibition.start_date, String).label('start_date'),
        Cast(Exhibition.end_date, String).label('end_date'),
        Gallery.name.label("gallery_name"),
        case(
            (liked_subquery.c.likes, 1),
            else_=0).label('liked')) \
        .join(Gallery, Gallery.id == Exhibition.gallery_id) \
        .outerjoin(liked_subquery, liked_subquery.c.exhibition_id == Exhibition.id) \
        
    return exhibitions

# [함수] 진행/예정/종료 전시 상태 (오늘 날짜와 비교)
def get_exhibition_status(exhibitions):

    today = datetime.today().date()  #오늘 날짜
    ongoing_exhibitions = []         #진행중 전시 
    upcoming_exhibitions = []        #예정중 전시
    ended_exhibitions = []           #지난 전시
    for exhibition in exhibitions:
        start_date = datetime.strptime(exhibition.start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(exhibition.end_date, '%Y-%m-%d').date()
        if start_date <= today and end_date >= today:
            ongoing_exhibitions.append(exhibition)
        elif start_date > today:
            upcoming_exhibitions.append(exhibition)
        elif end_date < today:
            ended_exhibitions.append(exhibition)
    data = {
        "ongoing_exhibitions": ongoing_exhibitions,
        "upcoming_exhibitions": upcoming_exhibitions,
        "ended_exhibitions": ended_exhibitions
        }

    return data

# 작가 팔로우
@artist_bp.route('/artist/<artist_id>/following', methods=['post'])
def following_artist(artist_id):
    existing_following_artist = FollowingArtist.query \
        .filter(FollowingArtist.user_id == session["user_id"], FollowingArtist.artist_id == artist_id) \
        .first()
    
    if existing_following_artist is not None:
        db.session.delete(existing_following_artist)
        db.session.commit()
        
        return "unfollowed"
    else:
        user_id = session["user_id"]
        followed_at = datetime.now()
        insertdb = FollowingArtist(id=str(uuid.uuid4()), user_id=user_id, artist_id=artist_id, followed_at=followed_at)
        db.session.add(insertdb)
        db.session.commit()

    return "followed"