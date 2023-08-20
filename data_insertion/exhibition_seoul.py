import os
import sys
import uuid
import datetime
from sqlalchemy import or_

from utils import load_secrets, fetch_api_data_json, get_address_from_gps

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from models.model import db, Exhibition, Gallery, GalleryAddress, Artist, ArtistExhibition


def insert_exhibition_seoul() :
    secrets = load_secrets()
    seoul_api_key = secrets["database"]["seoul_api_key"]
    seoul_api_url = f"http://openapi.seoul.go.kr:8088/{seoul_api_key}/json/ListExhibitionOfSeoulMOAInfo/1/723/"

    json_data = fetch_api_data_json(seoul_api_url)
    json_data = json_data['ListExhibitionOfSeoulMOAInfo']['row']
    insert_seoul_to_db(json_data)

def insert_seoul_to_db(data_dict):
    for data in data_dict:
        title = data['DP_NAME']
        title = title.replace('"', "&quot;")
        title = title.replace("'", "&apos;")
        start_date = datetime.datetime.strptime(data['DP_START'], '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(data['DP_END'], '%Y-%m-%d').date()
        thumbnail_img = data['DP_MAIN_IMG']
        description = data['DP_INFO']

        gallery_name = data['DP_PLACE']
        gallery_name = gallery_name.replace("(", " ")
        gallery_name = gallery_name.replace(")", " ") 
        gallery = Gallery.query \
            .filter(Gallery.name == gallery_name) \
            .all()
        if not gallery:
            new_gallery = Gallery(id=str(uuid.uuid4()), name=gallery_name)
            db.session.add(new_gallery)
        gallery = Gallery.query \
            .filter(Gallery.name == gallery_name) \
            .first()
        
        price = None
        if data['DP_VIEWCHARGE'] in ['무료', '무료관람', '무료 관람', '관람비 무료'] :
            price = 0

        exhibition = Exhibition.query \
            .filter(Exhibition.title==title) \
            .all()
        if not exhibition:
            exhibition_id = str(uuid.uuid4())
            new_exhib = Exhibition(id=exhibition_id, title=title, description=description, 
                                  start_date=start_date, end_date=end_date, thumbnail_img=thumbnail_img,
                                  gallery_id=gallery.id, price=price)
            db.session.merge(new_exhib)

        artist_list = data['DP_ARTIST'].split(',')
        for a in artist_list:
            a.strip()
            if '명' in a:
                artist_list.remove(a)
            elif not a:
                artist_list.remove(a)
            else :
                artist_id = str(uuid.uuid4())
                new_artist = Artist(id=artist_id, name=a)
                db.session.add(new_artist)
                new_artist_exhibition = ArtistExhibition(artist_id=artist_id, exhibition_id=exhibition_id)
                db.session.add(new_artist_exhibition)
    db.session.commit()