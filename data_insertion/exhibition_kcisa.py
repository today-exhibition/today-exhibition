import os
import sys

from utils import load_secrets, fetch_api_data, convert_xml, get_address_from_gps
from data_utils.encode import encode_exhibition_title, encode_date, encode_gallery_name
from data_utils.get_data import get_gallery_by_name, get_gallery_id_by_name, get_galleryaddress_by_id
from data_utils.make_instance import make_gallery_by_name, make_galleryaddress, make_exhibition
from data_utils.api_thumbnail_to_s3 import thumbnail_to_s3
from data_utils.remove_thumbnail import remove_thumbnail

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from models.model import db


def insert_kcisa_to_db(data_dict):
    for data in data_dict:
        if data['realmName'] == '미술':
            # Gallery
            gallery_name = encode_gallery_name(data['place'])
            gallery = get_gallery_by_name(gallery_name)
            if not gallery:
                make_gallery_by_name(gallery_name)
            gallery_id = get_gallery_id_by_name(gallery_name)
            
            # GalleryAddress (gps와 카카오지도 이용)
            gpsx = data['gpsX']
            gpsy = data['gpsY']
            area, address = get_address_from_gps(gpsx, gpsy)
            if area and address :
                gallery_address = get_galleryaddress_by_id(gallery_id)
                if not gallery_address:
                    make_galleryaddress(gallery_id, area, gpsx, gpsy, address)

            # Exhibition
            id = data['seq']
            title = encode_exhibition_title(data['title'])
            start_date = encode_date(data['startDate'], '%Y%m%d')
            end_date = encode_date(data['endDate'], '%Y%m%d')
            thumbnail_img = data['thumbnail']
            thumbnail_img, low_thumbnail_img = thumbnail_to_s3(id, thumbnail_img)
            make_exhibition(id, title, start_date, end_date, gallery_id, thumbnail_img, low_thumbnail_img)
    db.session.commit()
    remove_thumbnail(dirPath = "thumbnail_imgs")

def insert_exhibition_kcisa() :
    secrets = load_secrets()
    kcisa_api_url = "http://www.culture.go.kr/openapi/rest/publicperformancedisplays/period"
    kcisa_api_key = secrets["database"]["kcisa_api_key"]

    params ={'serviceKey' : kcisa_api_key,
            'rows' : '100',
            'cPage' : '1'}
    xml_data = fetch_api_data(kcisa_api_url, params)

    data_dict = convert_xml(xml_data)
    data_dict = data_dict['response']['msgBody']['perforList']
    insert_kcisa_to_db(data_dict)