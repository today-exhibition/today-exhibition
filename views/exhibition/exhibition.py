from flask import Blueprint, request, render_template
from models.model import Exhibition
from datetime import datetime

exhibition_bp = Blueprint('searchpage', __name__)

@exhibition_bp.route('/exhibition')
def exhibition():
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
                        .limit(20)

    return render_template('exhibition/exhibition.html', exhibitions=exhibitions, keyword=keyword)
