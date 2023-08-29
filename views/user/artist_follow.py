from flask import Blueprint, render_template, session
from sqlalchemy import func

from models.model import db, Artist, FollowingArtist
from decorators import check_user_login


artist_follow_bp = Blueprint('artist_follow', __name__)

@artist_follow_bp.route('/artist/follow')
@check_user_login
def artist_follow():
    user_id = session["user_id"]
    artist_list = db.session.query(
        Artist.id,
        Artist.name,
        func.count('*').label('follows')) \
        .join(FollowingArtist, FollowingArtist.artist_id == Artist.id) \
        .filter(FollowingArtist.user_id == user_id) \
        .group_by(FollowingArtist.artist_id) \
        .order_by(FollowingArtist.followed_at.desc()) \
        .all()
    
    return render_template('user/artist_follow.html', artist_list=artist_list, user_id=user_id)