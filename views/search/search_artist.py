from flask import Blueprint, request, render_template, session

from models.model import FollowingArtist
from views.search.search_exhibition import calc_pages
from views.search.search import get_search_artists

search_artist_bp = Blueprint('search_artist', __name__)

@search_artist_bp.route('/search/artist')
def search_artist():
    keyword = request.args.get('keyword', default="", type=str).strip()
    page = request.args.get('page', default=1, type=int)

    user_id = session.get('user_id', None)

    artists = get_search_artists(keyword).all()
    
    artist_count = len(artists)

    followed_artist_ids = []
    if user_id:
        followed_artist_ids = [follow.artist_id for follow in FollowingArtist.query.filter_by(user_id=user_id).all()]
    
    total_pages, current_page, page_data, page_list = calc_pages(artists, page)

    return render_template('search/search_artist.html', artists=page_data, keyword=keyword, artist_count=artist_count, user_id=user_id, followed_artist_ids=followed_artist_ids, total_pages=total_pages, current_page=current_page, page_list=page_list)
