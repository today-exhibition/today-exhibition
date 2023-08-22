from flask import Blueprint, render_template, session
from sqlalchemy import func
from datetime import datetime
from models.model import db, Artist, Exhibition, Gallery, ArtistExhibition, FollowingArtist
import uuid

artist_bp = Blueprint('artist', __name__)

@artist_bp.route('/artist/<id>')
def artist(id):
    # [작가디테일 > 작가 정보 조회]
    artist = db.session.query(
        Artist.name)\
        .filter(Artist.id == id)\
        .first()

    # [작가디테일 > 전시 정보 조회]
    exhibitions = db.session.query(
        Exhibition.id,
        Exhibition.title, 
        Gallery.name, 
        Exhibition.start_date, 
        Exhibition.end_date, 
        Exhibition.thumbnail_img)\
        .join(Gallery, Exhibition.gallery_id == Gallery.id)\
        .join(ArtistExhibition, ArtistExhibition.exhibition_id == Exhibition.id)\
        .join(Artist, Artist.id == ArtistExhibition.artist_id)\
        .filter(Artist.id == id)\
        .all()
    
    # [작가디테일 > 진행/예정/종료 전시 상태 (오늘 날짜와 비교)]
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


    return render_template('artist/artist.html', artist=artist, 
                            ongoing_exhibitions=ongoing_exhibitions,
                            upcoming_exhibitions=upcoming_exhibitions,                  
                            ended_exhibitions=ended_exhibitions, id=id)

# [작가디테일 > 작가 팔로우]
@artist_bp.route('/artist/<artist_id>/following', methods=['post'])
def following_exhibition(artist_id):
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