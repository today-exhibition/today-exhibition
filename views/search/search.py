from flask import Blueprint, request, render_template, jsonify, current_app
from models.model import db, Exhibition, Gallery, GalleryAddress
# Comment, User
from datetime import datetime
from sqlalchemy import func
import json


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
                        Gallery.name,
                        Exhibition.thumbnail_img
                        ) \
                        .filter(Exhibition.title.like('%' + keyword + '%')) \
                        .join(Gallery, Exhibition.gallery_id == Gallery.id) \
                        .order_by(Exhibition.start_date) \
                        .all()
    
    gallerys = Gallery.query \
                .with_entities(
                Gallery.id,
                Gallery.name,
                Gallery.thumbnail_img
                ) \
                .filter(Gallery.name.like('%' + keyword + '%')) \
                .order_by(Gallery.id) \
                .all()

    exhibition_count = len(exhibitions)
    exhibition_list = exhibitions[:3]

    gallery_count = len(gallerys)
    gallery_list = gallerys[:3]
    

    return render_template('search/search.html', exhibition_list=exhibition_list, keyword=keyword, exhibition_count=exhibition_count, gallery_count=gallery_count, gallery_list=gallery_list)

@search_bp.route('/search/exhibition')
def search_exhibition():
    keyword = request.args.get('keyword', default="", type=str).strip()
    sub_sorts = request.args.get('sub_sort')  # ongoing,free
    areas = request.args.get('area') 
    sort = request.args.get('sort') 
    print(areas)
    
    selected_sub_sorts = sub_sorts.split(',') if sub_sorts else [] # ['ongoing', 'free']
    selected_areas = areas.split(',') if areas else []
    print(selected_areas)

    current_datetime = datetime.now() 

    exhibitions_query = Exhibition.query \
                        .with_entities(
                        Exhibition.id,
                        Exhibition.title,
                        Exhibition.start_date,
                        Exhibition.end_date,
                        Gallery.name,
                        Exhibition.thumbnail_img,
                        func.substr(GalleryAddress.area, 1, 2)
                        ) \
                        .filter(Exhibition.title.like('%' + keyword + '%')) \
                        .join(Gallery, Exhibition.gallery_id == Gallery.id) \
                        .join(GalleryAddress, Gallery.id == GalleryAddress.gallery_id) \
                        .order_by(Exhibition.start_date) 
                   
    if selected_areas:
        exhibitions_query = exhibitions_query.filter(func.substr(GalleryAddress.area, 1, 2).in_(selected_areas))
        print(exhibitions_query)

    exhibitions = exhibitions_query.all()
    print(exhibitions)
    
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

@search_bp.route('/search/gallery')
def search_gallery():
    keyword = request.args.get('keyword', default="", type=str).strip()

    # exhibitions = Exhibition.query \
    #                 .with_entities(
    #                 Exhibition.id,
    #                 Exhibition.title,
    #                 Exhibition.start_date,
    #                 Exhibition.end_date,
    #                 Gallery.name,
    #                 Exhibition.thumbnail_img
    #                 ) \
    #                 .filter(Exhibition.title.like('%' + keyword + '%')) \
    #                 .join(Gallery, Exhibition.gallery_id == Gallery.id) \
    #                 .order_by(Exhibition.start_date) \
    #                 .all()
    
    
        
    gallerys = Gallery.query \
                .with_entities(
                Gallery.id,
                Gallery.name,
                Gallery.thumbnail_img
                ) \
                .filter(Gallery.name.like('%' + keyword + '%')) \
                .order_by(Gallery.id) \
                .all()
    
    gallery_count = len(gallerys)

    return render_template('search/search_gallery.html', gallerys=gallerys, keyword=keyword, gallery_count=gallery_count)