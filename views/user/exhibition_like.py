from flask import Blueprint, render_template, session
from sqlalchemy import func

from models.model import db, Exhibition, Gallery, LikeExhibition
from decorators import check_user_login


exhibition_like_bp = Blueprint('exhibition_like', __name__)

@exhibition_like_bp.route('/exhibition/like')
@check_user_login
def exhibition_like():
    user_id = session["user_id"]
    exhibition_list = db.session.query(
        Exhibition.id,
        Exhibition.title,
        Exhibition.start_date,
        Exhibition.end_date,
        Exhibition.thumbnail_img,
        Gallery.name,
        func.count('*').label('likes')) \
        .join(Gallery, Gallery.id == Exhibition.gallery_id) \
        .join(LikeExhibition, LikeExhibition.exhibition_id == Exhibition.id) \
        .filter(LikeExhibition.user_id == user_id) \
        .group_by(LikeExhibition.exhibition_id) \
        .order_by(LikeExhibition.liked_at.desc()) \
        .all()
    
    return render_template('user/exhibition_like.html', exhibition_list=exhibition_list, user_id=user_id)