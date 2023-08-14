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

@search_bp.route('/search/exhibition')
def search_exhibition():
    keyword = request.args.get('keyword', default="", type=str).strip()
    sort = request.args.get('sort')
    sub_sort = request.args.get('sub_sort')

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
    
    return render_template('search/search_exhibition.html', exhibitions=exhibitions, keyword=keyword, exhibition_count=exhibition_count)

@search_bp.route('/search/artist')
def search_artist():
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

@search_bp.route('/search/gallery')
def search_gallery():
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
        
    # gallerys = Gallery.query \
    #             .with_entities(
    #             Gallery.id,
    #             Gallery.name,
    #             Gallery.thumbnail_img
    #             ) \
    #             .filter(Gallery.name.like('%' + keyword + '%')) \
    #             .order_by(Gallery.id) \
    #             .limit(9)

    return render_template('search/search_gallery.html', exhibitions=exhibitions, keyword=keyword, exhibition_count=exhibition_count)