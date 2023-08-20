import math
import datetime

from flask import Blueprint, request, render_template, session
from sqlalchemy import func, or_, desc

from models.model import Exhibition, Gallery, GalleryAddress, LikeExhibition

search_exhibition_bp = Blueprint('search_exhibition', __name__)

@search_exhibition_bp.route('/search/exhibition')
def search_exhibition():
    keyword = request.args.get('keyword', default="", type=str).strip()
    sub_sorts = request.args.get('sub_sort') # ongoing,free
    areas = request.args.get('area') 
    sort = request.args.get('sort') 
    page = request.args.get('page', default=1, type=int)

    selected_sub_sorts = sub_sorts.split(',') if sub_sorts else []
    selected_areas = areas.split(',') if areas else []

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
                                    .order_by(desc(Exhibition.start_date)) \
    
    if sub_sorts:
        exhibitions_query = sub_sorts_filter(exhibitions_query, selected_sub_sorts)
    if areas:
        exhibitions_query = areas_filter(exhibitions_query, selected_areas)
    if sort:
        exhibitions_query = sort_filter(exhibitions_query, sort)
   
    exhibitions = exhibitions_query.all()
    
    exhibition_count = len(exhibitions)

    total_pages, current_page, page_data = calc_pages(exhibitions, page)

    # 사용자가 좋아요한 id 목록
    liked_exhibition_ids = []  
    if user_id:
        liked_exhibition_ids = [like.exhibition_id for like in LikeExhibition.query.filter_by(user_id=user_id).all()]
    
    return render_template('search/search_exhibition.html', exhibitions=page_data, keyword=keyword, exhibition_count=exhibition_count, user_id=user_id, liked_exhibition_ids=liked_exhibition_ids, sub_sorts=sub_sorts, areas=areas, sort=sort, total_pages=total_pages, current_page=current_page)

# 페이지 계산
def calc_pages(data, current_page):
    per_page = 12
    data_length = len(data)
    total_pages = math.ceil((data_length / per_page))
    start_index = per_page * (current_page -1)
    end_index = start_index + per_page
    page_data = data[start_index:end_index]

    return total_pages, current_page, page_data

# 전시중, 전시종료, 전시예정    
def sub_sorts_filter(query, selected_sub_sorts):
    sorts = []

    if 'ongoing' in selected_sub_sorts:
        sorts.append(Exhibition.start_date <= datetime.datetime.today())
    if 'ended' in selected_sub_sorts:
        sorts.append(Exhibition.end_date < datetime.datetime.today() - datetime.timedelta(days=1))
    if 'upcoming' in selected_sub_sorts:
        sorts.append(Exhibition.start_date > datetime.datetime.today())

    if sorts:
        return query.filter(or_(*sorts))
    else:
        return query

# 지역        
def areas_filter(query, selected_areas):
    if selected_areas:
        query = query.join(GalleryAddress, Gallery.id == GalleryAddress.gallery_id, isouter=True) \
                    .filter(func.substr(GalleryAddress.area, 1, 2).in_(selected_areas))
    return query
    
# 인기순(전체 하트순), 지금 주목받는 전시(일주일 동안 하트순), 추천 전시(큐레이팅 전시)
def sort_filter(query, selected_sort):
    if selected_sort == 'popularity':
        query = query.join(LikeExhibition, LikeExhibition.exhibition_id == Exhibition.id) \
                    .group_by(LikeExhibition.exhibition_id) \
                    .order_by(func.count('*').desc()) 
    if selected_sort == 'featured':
        query = query.join(LikeExhibition, LikeExhibition.exhibition_id == Exhibition.id) \
                    .filter(LikeExhibition.liked_at > datetime.datetime.today() - datetime.timedelta(weeks=1)) \
                    .group_by(LikeExhibition.exhibition_id) \
                    .order_by(func.count('*').desc())
    if selected_sort == 'recommended':
        query = query.order_by(func.random())

    return query