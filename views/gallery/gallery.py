from flask import Blueprint, render_template
from sqlalchemy import func
from datetime import datetime
from models.model import db, Artist, Exhibition, Gallery, GalleryAddress, ArtistExhibition

gallery_bp = Blueprint('gallery', __name__)

# ! [미술관디테일 > 미술관 정보 조회(미술관명, 운영시간, 휴관일, 주소, 연락처, 주차장, 홈페이지, 소개)]
# ? gallery 테이블에 adderess 컬럼이 사라졌다. -> 반영(2023.08.12)
@gallery_bp.route('/gallery/<id>')
def gallery(id):
    galleries = db.session.query(
                Gallery.name,
                Gallery.opening_hours,
                Gallery.holiday_info,
                GalleryAddress.address,
                Gallery.contact,
                Gallery.parking_yn,
                Gallery.homepage_url,
                Gallery.description)\
                .join(GalleryAddress, Gallery.id == GalleryAddress.gallery_id)\
                .filter(Gallery.id == id)\
                .all()
    
#! [미술관디테일 > 전시 정보 조회(전시명, 미술관명, 전시기간, 전시이미지)]
    exhibitions = db.session.query(
                Exhibition.title, 
                Gallery.name, 
                Exhibition.start_date, 
                Exhibition.end_date, 
                Exhibition.thumbnail_img)\
                .join(Gallery, Exhibition.gallery_id == Gallery.id)\
                .join(ArtistExhibition, ArtistExhibition.exhibition_id == Exhibition.id)\
                .join(Artist, Artist.id == ArtistExhibition.artist_id)\
                .filter(Artist.id == id).all()
    
#! [미술관디테일 > 진행/예정/종료 전시 상태 (오늘 날짜와 비교)]
    today = datetime.today().date()  #오늘 날짜
    ongoing_exhibitions = []       #진행중 전시 
    upcoming_exhibitions = []      #예정중 전시
    ended_exhibitions = []         #지난 전시

    for exhibition in exhibitions:
        if exhibition[2] <= today and exhibition[3] >= today:
            ongoing_exhibitions.append(exhibition)
        elif exhibition[2] > today:
            upcoming_exhibitions.append(exhibition)
        elif exhibition[3] < today:
            ended_exhibitions.append(exhibition)

    return render_template('gallery/gallery.html', galleries=galleries, 
                            ongoing_exhibitions=ongoing_exhibitions,
                            ongoing_count=len(ongoing_exhibitions),
                            upcoming_exhibitions=upcoming_exhibitions,
                            upcoming_count=len(upcoming_exhibitions),                    
                            ended_exhibitions=ended_exhibitions,
                            ended_count=len(ended_exhibitions), id=id)