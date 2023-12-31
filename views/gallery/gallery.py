from flask import Blueprint, render_template, session
from sqlalchemy import func
from datetime import datetime
from models.model import db, Gallery, GalleryAddress, FollowingGallery
from views.artist.artist import get_exhibition_data, get_exhibition_status
from views.search.search import get_followed_gallery_ids, get_liked_exhibition_ids
import uuid

gallery_bp = Blueprint('gallery', __name__)

# 미술관 디테일 (미술관, 전시상태, 작가팔로우, 미술관팔로우)
@gallery_bp.route('/gallery/<id>')
def gallery(id):
    user_id = session.get('user_id', None)

    gallery = get_gallery_data(id)
    exhibitions = get_exhibition_data(user_id)\
        .filter(Gallery.id == id)\
        .all() 
    # exhibition_status = get_exhibition_status(exhibitions)
    
    followed_gallery_ids = get_followed_gallery_ids(user_id)
    liked_exhibition_ids = get_liked_exhibition_ids(user_id)

    data = {
        "gallery": [gallery._asdict()],
        "exhibitions": [row._asdict() for row in exhibitions],
        "user_id": user_id,
        "followed_gallery_ids": followed_gallery_ids,        
        "liked_exhibition_ids": liked_exhibition_ids
        }
    
    return render_template('gallery/gallery.html', data=data)

# [함수] 미술관 정보
def get_gallery_data(id):
    gallery = db.session.query(
        Gallery.id,
        Gallery.name,
        Gallery.thumbnail_img,
        Gallery.opening_hours,
        Gallery.holiday_info,
        GalleryAddress.address,
        Gallery.contact,
        Gallery.parking_yn,
        Gallery.homepage_url,
        Gallery.description,
        FollowingGallery.gallery_id)\
        .join(GalleryAddress, Gallery.id == GalleryAddress.gallery_id, isouter = True)\
        .join(FollowingGallery, Gallery.id == FollowingGallery.gallery_id, isouter = True) \
        .filter(Gallery.id == id)\
        .first()
    
    return gallery
    
# 미술관 팔로우
@gallery_bp.route('/gallery/<gallery_id>/following', methods=['post'])
def following_gallery(gallery_id):
    if "user_id" not in session:
        return "login_required"

    existing_following_gallery = FollowingGallery.query \
        .filter(FollowingGallery.user_id == session["user_id"], FollowingGallery.gallery_id == gallery_id) \
        .first()
    
    if existing_following_gallery is not None:
        db.session.delete(existing_following_gallery)
        db.session.commit()

        return "unfollowed"
    else:
        user_id = session["user_id"]
        followed_at = datetime.now()
        insertdb = FollowingGallery(id=str(uuid.uuid4()), user_id=user_id, gallery_id=gallery_id, followed_at=followed_at)
        db.session.add(insertdb)
        db.session.commit()

        return "followed"