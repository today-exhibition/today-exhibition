from flask import Blueprint, render_template, session
from sqlalchemy import func, Cast, String

from models.model import db, Exhibition, Gallery, LikeExhibition


exhibition_like_bp = Blueprint('exhibition_like', __name__)

@exhibition_like_bp.route('/exhibition/like')
def exhibition_like():
    if "user_id" not in session:
        return render_template("user/login.html")
    
    user_id = session["user_id"]
    exhibition_list = db.session.query(
        Exhibition.id.label('exhibition_id'),
        Exhibition.title.label("exhibition_title"),
        Exhibition.thumbnail_img,
        Cast(Exhibition.start_date, String).label('start_date'),
        Cast(Exhibition.end_date, String).label('end_date'),
        Gallery.name.label("gallery_name"),
        func.count('*').label('liked')) \
        .join(Gallery, Gallery.id == Exhibition.gallery_id) \
        .join(LikeExhibition, LikeExhibition.exhibition_id == Exhibition.id) \
        .filter(LikeExhibition.user_id == user_id) \
        .group_by(LikeExhibition.exhibition_id) \
        .order_by(LikeExhibition.liked_at.desc()) \
        .all()

    result = {}
    result['exhibitions'] = [row._asdict() for row in exhibition_list]
    
    return render_template('user/exhibition_like.html', data=result)