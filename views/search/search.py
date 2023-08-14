from flask import Blueprint, request, render_template
from models.model import Exhibition
# , Gallery, Comment, User
from datetime import datetime
from sqlalchemy import func


search_bp = Blueprint('search', __name__)

@search_bp.route('/search')
def search():
    keyword = request.args.get('keyword', default="", type=str).strip()
  
    exhibitions = Exhibition.query \
                        .with_entities(
                        Exhibition.id,
                        Exhibition.title,
                        Exhibition.start_date,
                        Exhibition.end_date,
                        Exhibition.gallery_id,
                        Exhibition.thumbnail_img
                        ) \
                        .filter(Exhibition.title.like('%' + keyword + '%')) \
                        .order_by(Exhibition.start_date) \
                        .all()

    exhibition_count = len(exhibitions)
    exhibition_list = exhibitions[:3]
    

    return render_template('search/search.html', exhibition_list=exhibition_list, keyword=keyword, exhibition_count=exhibition_count)