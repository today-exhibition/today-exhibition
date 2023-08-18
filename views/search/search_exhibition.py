from datetime import datetime, timedelta
from flask import Blueprint, request, render_template, session
from sqlalchemy import func

from models.model import Exhibition, Gallery, GalleryAddress, LikeExhibition

search_exhibition_bp = Blueprint('search_exhibition', __name__)

@search_exhibition_bp.route('/search/exhibition')
def search_exhibition():
    keyword = request.args.get('keyword', default="", type=str).strip()
    sub_sorts = request.args.get('sub_sort') # ongoing,free
    areas = request.args.get('area') 
    sort = request.args.get('sort') 

    selected_sub_sorts = sub_sorts.split(',') if sub_sorts else []
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