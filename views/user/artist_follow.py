from flask import Blueprint, render_template, session
from sqlalchemy import func

from models.model import ArtistExhibition, Exhibition, db, Artist, FollowingArtist
from decorators import check_user_login


artist_follow_bp = Blueprint('artist_follow', __name__)

@artist_follow_bp.route('/artist/follow')
@check_user_login
def artist_follow():
    user_id = session["user_id"]
    artist_list = db.session.query(
        Artist.id,
        Artist.name,
        Artist.thumbnail_img.label('artist_thumbnail_img'),
        Exhibition.thumbnail_img.label('exhibition_thumbnail_img'),
        func.count('*').label('follows')) \
        .join(FollowingArtist, FollowingArtist.artist_id == Artist.id) \
        .join(ArtistExhibition, Artist.id == ArtistExhibition.artist_id) \
        .join(Exhibition, ArtistExhibition.exhibition_id == Exhibition.id) \
        .filter(FollowingArtist.user_id == user_id) \
        .group_by(FollowingArtist.artist_id) \
        .order_by(FollowingArtist.followed_at.desc()) \
        .all()
    
    result = {}
    result['artists'] = [row._asdict() for row in artist_list]
 
    return render_template('user/artist_follow.html', data=result)