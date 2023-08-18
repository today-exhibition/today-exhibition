from flask import Blueprint, request, render_template

from models.model import Exhibition, Gallery

search_artist_bp = Blueprint('search_artist', __name__)

@search_artist_bp.route('/search/artist')
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
