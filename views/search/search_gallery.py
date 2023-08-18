from flask import Blueprint, request, render_template, session

from models.model import Gallery, FollowingGallery

search_gallery_bp = Blueprint('search_gallery', __name__)

@search_gallery_bp.route('/search/gallery')
def search_gallery():
    keyword = request.args.get('keyword', default="", type=str).strip()

    user_id = session.get('user_id', None)

    gallerys = Gallery.query \
                .with_entities(
                Gallery.id,
                Gallery.name,
                Gallery.thumbnail_img,
                FollowingGallery.gallery_id
                ) \
                .filter(Gallery.name.like('%' + keyword + '%')) \
                .join(FollowingGallery, Gallery.id == FollowingGallery.gallery_id, isouter = True) \
                .order_by(Gallery.id) \
                .all()
    
    gallery_count = len(gallerys)

    followed_gallery_ids = []
    if user_id:
        followed_gallery_ids = [follow.gallery_id for follow in FollowingGallery.query.filter_by(user_id=user_id).all()]

    return render_template('search/search_gallery.html', gallerys=gallerys, keyword=keyword, gallery_count=gallery_count, user_id=user_id, followed_gallery_ids=followed_gallery_ids)