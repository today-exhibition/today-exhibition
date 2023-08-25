from flask import Blueprint, render_template, session
from sqlalchemy import func
from datetime import datetime
from models.model import db, Artist, Exhibition, Gallery, ArtistExhibition, FollowingArtist
from views.search.search import get_followed_artist_ids, get_liked_exhibition_ids
import uuid

artist_bp = Blueprint('artist', __name__)

# 작가 디테일(작가명, 전시상태, 작가팔로우, 전시좋아요)
@artist_bp.route('/artist/<id>')
def artist(id):
    artist = get_artist_data(id)\
        .filter(Artist.id == id)\
        .first()    
    exhibitions = get_exhibition_data(id)\
        .join(ArtistExhibition, ArtistExhibition.exhibition_id == Exhibition.id)\
        .join(Artist, Artist.id == ArtistExhibition.artist_id)\
        .filter(Artist.id == id)\
        .all()    
    exhibition_status = get_exhibition_status(exhibitions)   
    
    user_id = session.get('user_id', None)
    followed_artist_ids = get_followed_artist_ids(user_id)
    liked_exhibition_ids = get_liked_exhibition_ids(user_id)

    data = {
        "id": id,
        "artist": artist,
        "exhibitions": exhibitions,
        "exhibition_status": exhibition_status,
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
def get_exhibition_data(id):
    exhibitions = db.session.query(
        Exhibition.id,
        Exhibition.title, 
        Gallery.name, 
        Exhibition.start_date, 
        Exhibition.end_date, 
        Exhibition.thumbnail_img)\
        .join(Gallery, Exhibition.gallery_id == Gallery.id)
    return exhibitions

# [함수] 진행/예정/종료 전시 상태 (오늘 날짜와 비교)
def get_exhibition_status(exhibitions):
    today = datetime.today().date()  #오늘 날짜
    ongoing_exhibitions = []         #진행중 전시 
    upcoming_exhibitions = []        #예정중 전시
    ended_exhibitions = []           #지난 전시
    for exhibition in exhibitions:
        if exhibition.start_date <= today and exhibition.end_date >= today:
            ongoing_exhibitions.append(exhibition)
        elif exhibition.start_date > today:
            upcoming_exhibitions.append(exhibition)
        elif exhibition.end_date < today:
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
    result = following_artist(artist_id)

    return result

# [함수] 작가 팔로우 처리
def following_artist(artist_id):
    existing_following_artist = FollowingArtist.query\
        .filter(FollowingArtist.user_id == session["user_id"], FollowingArtist.artist_id == artist_id)\
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