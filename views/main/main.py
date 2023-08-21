from flask import Blueprint, render_template, session

from models.model import db, User, Exhibition, Gallery


main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def main():
    exhibitions = []
    exhibition_id = [247582, 247582, 247582]
    image_url = ['/img/main/247582/247582-1.png', '/img/main/247582/247582-2.png', '/img/main/247582/247582-3.png']
    
    for id in exhibition_id:
        exhibition = db.session.query(Exhibition.id, Exhibition.title, Gallery.name.label("gallery_name"), Exhibition.start_date, Exhibition.end_date, Exhibition.thumbnail_img, Exhibition.description)\
            .join(Gallery, Exhibition.gallery_id == Gallery.id)\
            .filter(Exhibition.id == id).first()
        exhibitions.append(exhibition)
    return render_template('main/main.html', exhibitions=exhibitions, image_url=image_url)