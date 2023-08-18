from flask import Blueprint, request, render_template, session
from models.model import db, Exhibition, Gallery, GalleryAddress, LikeExhibition, FollowingGallery
from datetime import datetime, timedelta
from sqlalchemy import func
import uuid


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

@search_bp.route('/search/exhibition/<exhibition_id>/like', methods=['post'])
def like_exhibition(exhibition_id):
    if "user_id" not in session:
        return "login_required"
    
    existing_like = LikeExhibition.query.filter(LikeExhibition.user_id == session["user_id"], LikeExhibition.exhibition_id == exhibition_id).first()
    
    if existing_like is not None:
        db.session.delete(existing_like)
        db.session.commit()
        return "unliked"
    else:
        user_id = session["user_id"]
        liked_at = datetime.now()
        insertdb = LikeExhibition(id=str(uuid.uuid4()), user_id=user_id, exhibition_id=exhibition_id, liked_at=liked_at)
        db.session.add(insertdb)
        db.session.commit()
    return "liked"

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

@search_bp.route('/search/exhibition')
def search_exhibition():
    keyword = request.args.get('keyword', default="", type=str).strip()
    sub_sorts = request.args.get('sub_sort') # ongoing,free
    areas = request.args.get('area') 
    sort = request.args.get('sort') 

    selected_sub_sorts = sub_sorts.split(',') if sub_sorts else [] # ['ongoing', 'free']
    selected_areas = areas.split(',') if areas else []

    current_datetime = datetime.now() 

    user_id = session.get('user_id', None)

    exhibitions_query = Exhibition.query \
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
                        .order_by(Exhibition.start_date) 
                   
    if 'ongoing' in selected_sub_sorts or 'ended' in selected_sub_sorts or 'upcoming' in selected_sub_sorts:
        ongoing_condition = Exhibition.start_date <= current_datetime
        ended_condition = Exhibition.end_date < current_datetime - timedelta(days=1)
        upcoming_condition = Exhibition.start_date > current_datetime
        
        if 'ongoing' in selected_sub_sorts and 'ended' in selected_sub_sorts and 'upcoming' in selected_sub_sorts:
            exhibitions_query = exhibitions_query.filter(
                ongoing_condition | ended_condition | upcoming_condition
            )
        elif 'ongoing' in selected_sub_sorts and 'ended' in selected_sub_sorts:
            exhibitions_query = exhibitions_query.filter(ongoing_condition | ended_condition)
        elif 'ongoing' in selected_sub_sorts and 'upcoming' in selected_sub_sorts:
            exhibitions_query = exhibitions_query.filter(ongoing_condition | upcoming_condition)
        elif 'ended' in selected_sub_sorts and 'upcoming' in selected_sub_sorts:
            exhibitions_query = exhibitions_query.filter(ended_condition | upcoming_condition)
        elif 'ongoing' in selected_sub_sorts:
            exhibitions_query = exhibitions_query.filter(ongoing_condition)
        elif 'ended' in selected_sub_sorts:
            exhibitions_query = exhibitions_query.filter(ended_condition)
        elif 'upcoming' in selected_sub_sorts:
            exhibitions_query = exhibitions_query.filter(upcoming_condition)
    

    if selected_areas:
        exhibitions_query = exhibitions_query.filter(func.substr(GalleryAddress.area, 1, 2).in_(selected_areas))
        
    exhibitions = exhibitions_query.all()
    
    exhibition_count = len(exhibitions)

    # 사용자가 좋아요한 id 목록
    liked_exhibition_ids = []  
    if user_id:
        liked_exhibition_ids = [like.exhibition_id for like in LikeExhibition.query.filter_by(user_id=user_id).all()]
    
    return render_template('search/search_exhibition.html', exhibitions=exhibitions, keyword=keyword, exhibition_count=exhibition_count, user_id=user_id, liked_exhibition_ids=liked_exhibition_ids)

@search_bp.route('/search/artist')
def search_artist():
    keyword = request.args.get('keyword', default="", type=str).strip()

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
                    .order_by(Exhibition.start_date) \
                    .all()
    exhibition_count = len(exhibitions)
    # artists = Artist.query \
    #             .with_entities(
    #             Artist.id,
    #             Artist.name,
    #             Artist.thumbnail_img
    #             ) \
    #             .filter(Artist.name.like('%' + keyword + '%')) \
    #             .order_by(Artist.id) \
    #             .limit(9)

    return render_template('search/search_artist.html', exhibitions=exhibitions, keyword=keyword, exhibition_count=exhibition_count)

@search_bp.route('/search/gallery')
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