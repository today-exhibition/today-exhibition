from flask import Blueprint, render_template, session
from sqlalchemy import func

from models.model import Exhibition, db, Gallery, FollowingGallery
from decorators import check_user_login


gallery_follow_bp = Blueprint('gallery_follow', __name__)

@gallery_follow_bp.route('/gallery/follow')
@check_user_login
def gallery_follow():
    user_id = session["user_id"]
    gallery_list = db.session.query(
        Gallery.id,
        Gallery.name,
        Gallery.thumbnail_img.label('gallery_thumbnail_img'),
        Exhibition.thumbnail_img.label('exhibition_thumbnail_img'),
        func.count('*').label('follows')) \
        .join(Exhibition, Gallery.id == Exhibition.gallery_id) \
        .join(FollowingGallery, FollowingGallery.gallery_id == Gallery.id) \
        .filter(FollowingGallery.user_id == user_id) \
        .group_by(FollowingGallery.gallery_id) \
        .order_by(FollowingGallery.followed_at.desc()) \
        .all()
    
    result = {}
    result['galleries'] = [row._asdict() for row in gallery_list]
   
    return render_template('user/gallery_follow.html', data=result)