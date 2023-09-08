from flask import Blueprint, request, render_template, session

from views.search.search_exhibition import calc_pages
from views.search.search import get_artists

search_artist_bp = Blueprint('search_artist', __name__)

@search_artist_bp.route('/search/artist')
def search_artist():
    keyword = request.args.get('keyword', default="", type=str).strip()
    page = request.args.get('page', default=1, type=int)
    user_id = session.get('user_id', None)

    artists = get_artists(user_id, keyword).all()
    artist_count = len(artists)

    total_pages, current_page, page_data, page_list = calc_pages(artists, page)

    data = {
        "artists": [row._asdict() for row in page_data],
        "keyword": keyword,
        "artist_count": artist_count,
        "total_pages": total_pages,
        "current_page": current_page,
        "page_list": page_list
    }

    return render_template('search/search_artist.html', data=data)
