import os
import sys
import requests
import json
import datetime
import uuid

from utils import load_secrets, fetch_api_data

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from models.model import db, Gallery, GalleryAddress, GalleryOpeningHour

    
def insert_molit_to_db(data_dict):
    for data in data_dict:
        properties = data['properties']
        
        # gallery
        name = properties['mus_nam']

        if '박물관' not in name:
            contact = properties['opr_tel']
            holiday_info = properties['hdy_inf']

            gallery = Gallery.query \
                .filter(Gallery.name==name) \
                .all()
            if not gallery:
                new_gallery = Gallery(id=str(uuid.uuid4()), name=name, contact=contact, holiday_info=holiday_info)
                db.session.add(new_gallery)
            
            gallery = Gallery.query \
                .filter(Gallery.name==name) \
                .one()
            
            # TODO: area1, area2 가공하도록 코드 변경
            # TODO: gpsx, gpsy 지도 검색을 통해 받아오도록 코드 변경
            # gallery_address
            address = properties['new_adr']
            geometry = data['geometry']
            if geometry['type'] == 'Point' :
                gpsx = geometry['coordinates'][0]
                gpsy = geometry['coordinates'][1]
                gallery_address = GalleryAddress.query \
                    .filter(GalleryAddress.gallery_id==gallery.id) \
                    .all()
                if not gallery_address:
                    new_gallery_address = GalleryAddress(gallery_id=gallery.id, gpsx=gpsx, gpsy=gpsy, address=address)
            else : 
                gallery_address = GalleryAddress.query \
                    .filter(GalleryAddress.gallery_id==gallery.id) \
                    .one()
                if not gallery_address:
                    new_gallery_address = GalleryAddress(gallery_id=gallery.id, address=address)
            db.session.add(new_gallery_address)

            # gallery_openinghour
            weekday_open_hhmm = datetime.datetime.strptime(properties['wds_tme'], '%H:%M').time()
            weekday_close_hhmm = datetime.datetime.strptime(properties['wde_tme'], '%H:%M:%S.%f').time()            
            holiday_open_hhmm = datetime.datetime.strptime(properties['hds_tme'], '%H:%M').time()
            holiday_close_hhmm = datetime.datetime.strptime(properties['hde_tme'], '%H:%M:%S.%f').time()
            
            gallery_opening_hour = GalleryOpeningHour.query \
                .filter(GalleryOpeningHour.gallery_id==gallery.id) \
                .all()
            if not gallery_opening_hour:
                new_gallery_opening_hour = GalleryOpeningHour(gallery_id=gallery.id, weekday_open_hhmm=weekday_open_hhmm, weekday_close_hhmm=weekday_close_hhmm, holiday_open_hhmm=holiday_open_hhmm, holiday_close_hhmm=holiday_close_hhmm)
            db.session.add(new_gallery_opening_hour)
    db.session.commit()

def insert_gallery_molit() :
    secrets = load_secrets()
    molit_api_url = "http://api.vworld.kr/req/data"
    molit_api_key = secrets["database"]["molit_api_key"]

    params ={'key' : molit_api_key,
            'size' : '1000',
            'request' : 'GetFeature',
            'data' : 'LT_P_DGMUSEUMART',
            'domain' : 'http://127.0.0.1:5000/',
            'geomFilter' : 'BOX(124, 33, 132, 43)'}
    data = fetch_api_data(molit_api_url, params)

    data_dict = json.loads(data)
    data_dict = data_dict['response']['result']['featureCollection']['features']

    insert_molit_to_db(data_dict)
