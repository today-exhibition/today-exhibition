import os
import sys
import uuid

from utils import load_secrets, fetch_api_data_json
from data_utils.encode import encode_exhibition_title, encode_date, encode_gallery_name, encode_artist_name, is_free, is_artist
from data_utils.get_data import get_gallery_by_name, get_gallery_id_by_name, get_exhibition_by_title
from data_utils.make_instance import make_gallery_by_name, make_artist, make_artistexhibition
from data_utils.api_thumbnail_to_s3 import thumbnail_to_s3
from data_utils.remove_thumbnail import remove_thumbnail

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from models.model import db, Exhibition


def insert_seoul_to_db(data_dict):
    for data in data_dict:
        # Gallery
        gallery_name = encode_gallery_name(data['DP_PLACE'])
        gallery = get_gallery_by_name(gallery_name)
        if not gallery:
            make_gallery_by_name(gallery_name)
        gallery_id = get_gallery_id_by_name(gallery_name)

        # Exhibition
        title = encode_exhibition_title(data['DP_NAME'])
        start_date = encode_date(data['DP_START'], '%Y-%m-%d')
        end_date = encode_date(data['DP_END'], '%Y-%m-%d')
        thumbnail_img = data['DP_MAIN_IMG']
        description = data['DP_INFO']

        price = None
        if is_free(data['DP_VIEWCHARGE']):
            price = 0
            
        exhibition = get_exhibition_by_title(title)
        if not exhibition:
            exhibition_id = str(uuid.uuid4())
            thumbnail_img = thumbnail_to_s3(id, thumbnail_img)
            new_exhib = Exhibition(id=exhibition_id, title=title, description=description, 
                                  start_date=start_date, end_date=end_date, thumbnail_img=thumbnail_img, 
                                  gallery_id=gallery_id, price=price)
            db.session.merge(new_exhib)
        else:
            exhibition_id = exhibition[0].id
        
        # Artist, ArtistExhibition
        artist_list = encode_artist_name(data['DP_ARTIST'])
        for a in artist_list:
            a.strip()
            if is_artist(a) :
                artist_id = str(uuid.uuid4())
                make_artist(artist_id, a)
                make_artistexhibition(artist_id, exhibition_id)
            else:
                artist_list.remove(a)
    db.session.commit()
    remove_thumbnail(dirPath = "thumbnail_imgs")

def insert_exhibition_seoul() :
    secrets = load_secrets()
    seoul_api_key = secrets["database"]["seoul_api_key"]
    seoul_api_url = f"http://openapi.seoul.go.kr:8088/{seoul_api_key}/json/ListExhibitionOfSeoulMOAInfo/1/723/"

    json_data = fetch_api_data_json(seoul_api_url)
    json_data = json_data['ListExhibitionOfSeoulMOAInfo']['row']
    insert_seoul_to_db(json_data)