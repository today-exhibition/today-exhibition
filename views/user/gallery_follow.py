from flask import Blueprint, render_template, session
from sqlalchemy import func

from models.model import db, Gallery, FollowingGallery


gallery_follow_bp = Blueprint('gallery_follow', __name__)

@gallery_follow_bp.route('/gallery/follow')
def gallery_follow():
    if "user_id" not in session:
        return render_template("user/login.html")
    
    user_id = session["user_id"]
    gallery_list = db.session.query(
        Gallery.id,
        Gallery.name,
        func.count('*').label('follows')) \
        .join(FollowingGallery, FollowingGallery.gallery_id == Gallery.id) \
        .filter(FollowingGallery.user_id == user_id) \
        .group_by(FollowingGallery.gallery_id) \
        .order_by(FollowingGallery.followed_at.desc()) \
        .all()
    
    return render_template('user/gallery_follow.html', gallery_list=gallery_list, user_id=user_id)