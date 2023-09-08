from flask import Blueprint, request, render_template, session

from views.search.search_exhibition import calc_pages
from views.search.search import get_galleries

search_gallery_bp = Blueprint('search_gallery', __name__)

@search_gallery_bp.route('/search/gallery')
def search_gallery():
    keyword = request.args.get('keyword', default="", type=str).strip()
    page = request.args.get('page', default=1, type=int)
    user_id = session.get('user_id', None)

    gallerys = get_galleries(user_id, keyword).all()
    gallery_count = len(gallerys)

    total_pages, current_page, page_data, page_list = calc_pages(gallerys, page)
    data = {
        "galleries": [row._asdict() for row in page_data],
        "keyword": keyword,
        "gallery_count": gallery_count,
        "total_pages": total_pages,
        "current_page": current_page,
        "page_list": page_list
    }

    return render_template('search/search_gallery.html', data=data)