from datetime import datetime
import uuid

from flask import Blueprint, request, render_template, session

from models.model import db, Exhibition, Gallery, GalleryAddress, LikeExhibition, FollowingGallery

search_bp = Blueprint('search', __name__)

@search_bp.route('/search')
def search():
    keyword = request.args.get('keyword', default="", type=str).strip()

    user_id = session.get('user_id', None)

    exhibitions = Exhibition.query \
                        .with_entities(
                            Exhibition.id,
                            Exhibition.title,
                            Exhibition.start_date,
                            Exhibition.end_date,
                            Gallery.name,
                            Exhibition.thumbnail_img
                        ) \
                        .filter(Exhibition.title.like('%' + keyword + '%')) \
                        .join(Gallery, Exhibition.gallery_id == Gallery.id) \
                        .join(GalleryAddress, Gallery.id == GalleryAddress.gallery_id, isouter=True) \
                        .order_by(Exhibition.start_date) \
                        .all()
           
    gallerys = Gallery.query \
                .with_entities(
                Gallery.id,
                Gallery.name,
                Gallery.thumbnail_img,
                ) \
                .filter(Gallery.name.like('%' + keyword + '%')) \
                .join(FollowingGallery, Gallery.id == FollowingGallery.gallery_id, isouter = True) \
                .order_by(Gallery.id) \
                .all()

    exhibition_count = len(exhibitions)
    exhibition_list = exhibitions[:3]

    gallery_count = len(gallerys)
    gallery_list = gallerys[:3]

    # 사용자가 좋아요, 팔로우한 id 목록
    liked_exhibition_ids = []  
    if user_id:
        liked_exhibition_ids = [like.exhibition_id for like in LikeExhibition.query.filter_by(user_id=user_id).all()]

    followed_gallery_ids = []
    if user_id:
        followed_gallery_ids = [follow.gallery_id for follow in FollowingGallery.query.filter_by(user_id=user_id).all()]

    return render_template('search/search.html', exhibition_list=exhibition_list, keyword=keyword, exhibition_count=exhibition_count, gallery_count=gallery_count, gallery_list=gallery_list, user_id=user_id, liked_exhibition_ids=liked_exhibition_ids, followed_gallery_ids=followed_gallery_ids)

@search_bp.route('/search/gallery/<gallery_id>/following', methods=['post'])
def following_exhibition(gallery_id):
    if "user_id" not in session:
        return "login_required"
    
    existing_following_gallery = FollowingGallery.query.filter(FollowingGallery.user_id == session["user_id"], FollowingGallery.gallery_id == gallery_id).first()
    
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
