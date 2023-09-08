import math
import datetime

from flask import Blueprint, request, render_template, session
from sqlalchemy import func, or_

from models.model import Exhibition, Gallery, GalleryAddress, LikeExhibition
from views.search.search import get_exhibitions

search_exhibition_bp = Blueprint('search_exhibition', __name__)

@search_exhibition_bp.route('/search/exhibition')
def search_exhibition():
    keyword = request.args.get('keyword', default="", type=str).strip()
    page = request.args.get('page', default=1, type=int)
    user_id = session.get('user_id', None)
    sub_sorts = request.args.get('sub_sort') if request.args.get('sub_sort') else "" # ongoing, ended, upcoming
    areas = request.args.get('area') if request.args.get('areas') else "" # 서울, 경기, 강원, 대전
    sort = request.args.get('sort') if request.args.get('sort') else "" # popularity, featured, recommended

    selected_sub_sorts = sub_sorts.split(',') if sub_sorts else []
    selected_areas = areas.split(',') if areas else []

    exhibitions_query = get_exhibitions(user_id, keyword)
    
    if sub_sorts:
        exhibitions_query = sub_sorts_filter(exhibitions_query, selected_sub_sorts)
    if areas:
        exhibitions_query = areas_filter(exhibitions_query, selected_areas)
    if sort:
        exhibitions_query = sort_filter(exhibitions_query, sort)
   
    exhibitions = exhibitions_query.all()
    exhibition_count = len(exhibitions)

    total_pages, current_page, page_data, page_list = calc_pages(exhibitions, page)
    page_data = [row._asdict() for row in page_data]

    data = {
        "exhibitions": page_data,
        "keyword": keyword,
        "exhibition_count": exhibition_count,
        "sub_sorts": sub_sorts,
        "areas": areas,
        "sort": sort,
        "total_pages": total_pages,
        "current_page": current_page,
        "page_list": page_list
    }
    
    return render_template('search/search_exhibition.html', data=data)

# 페이지 계산
def calc_pages(data, current_page):
    per_page = 15
    data_length = len(data)
    total_pages = math.ceil((data_length / per_page))
    start_index = per_page * (current_page -1)
    end_index = start_index + per_page
    page_data = data[start_index:end_index]
    page_list = calc_page_list(current_page, total_pages)

    return total_pages, current_page, page_data, page_list

def calc_page_list(current_page, total_page):
    if current_page <= 2:
        page_list = [_ for _ in range(1, min(total_page+1, 6))]
    elif current_page == total_page or current_page == total_page - 1:
        page_list = [_ for _ in range(max(1, total_page-4), total_page+1)]
    else:
        page_list = [_ for _ in range(current_page-2, current_page+2+1)]

    return page_list

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
        query = query \
            .join(GalleryAddress, Gallery.id == GalleryAddress.gallery_id, isouter=True) \
            .filter(GalleryAddress.area.in_(selected_areas))
        
    return query
    
# 인기순(전체 하트순), 지금 주목받는 전시(일주일 동안 하트순), 추천 전시(큐레이팅 전시)
def sort_filter(query, selected_sort):
    if selected_sort == 'popularity':
        query = query \
            .join(LikeExhibition, LikeExhibition.exhibition_id == Exhibition.id) \
            .group_by(LikeExhibition.exhibition_id) \
            .order_by(func.count('*').desc()) 
    if selected_sort == 'featured':
        query = query \
            .join(LikeExhibition, LikeExhibition.exhibition_id == Exhibition.id) \
            .filter(LikeExhibition.liked_at > datetime.datetime.today() - datetime.timedelta(weeks=1)) \
            .group_by(LikeExhibition.exhibition_id) \
            .order_by(func.count('*').desc())
    if selected_sort == 'recommended':
        query = query

    return query