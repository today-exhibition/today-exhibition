from flask import Blueprint, render_template, session
from sqlalchemy import func
from datetime import datetime
from models.model import db, Artist, Exhibition, Gallery, GalleryAddress, FollowingGallery
import uuid

gallery_bp = Blueprint('gallery', __name__)

@gallery_bp.route('/gallery/<id>')
def gallery(id):
    # [미술관디테일 > 미술관 정보 조회]
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
    
    # [미술관디테일 > 전시 정보 조회]
    exhibitions = db.session.query(
        Exhibition.id,
        Exhibition.title, 
        Gallery.name, 
        Exhibition.start_date, 
        Exhibition.end_date, 
        Exhibition.thumbnail_img)\
        .join(Gallery, Exhibition.gallery_id == Gallery.id)\
        .filter(Gallery.id == id).all()
    
    # [미술관디테일 > 진행/예정/종료 전시 상태 (오늘 날짜와 비교)]
    today = datetime.today().date()  #오늘 날짜
    ongoing_exhibitions = []         #진행중 전시 
    upcoming_exhibitions = []        #예정중 전시
    ended_exhibitions = []           #지난 전시

    for exhibition in exhibitions:
        if exhibition.start_date <= today and exhibition.end_date >= today:
            ongoing_exhibitions.append(exhibition)
        elif exhibition.start_date > today:
            upcoming_exhibitions.append(exhibition)
        elif exhibition.end_date < today:
            ended_exhibitions.append(exhibition)

    return render_template('gallery/gallery.html', gallery=gallery, 
                            ongoing_exhibitions=ongoing_exhibitions,
                            ongoing_count=len(ongoing_exhibitions),
                            upcoming_exhibitions=upcoming_exhibitions,
                            upcoming_count=len(upcoming_exhibitions),                    
                            ended_exhibitions=ended_exhibitions,
                            ended_count=len(ended_exhibitions), id=id)

# [미술관디테일 > 미술관 팔로우]
@gallery_bp.route('/gallery/<gallery_id>/following', methods=['post'])
def following_exhibition(gallery_id):
    existing_following_gallery = FollowingGallery.query\
        .filter(FollowingGallery.user_id == session["user_id"], FollowingGallery.gallery_id == gallery_id)\
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