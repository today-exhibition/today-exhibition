import os
import sys
import uuid
import datetime

from utils import load_secrets, fetch_api_data, convert_xml

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from models.model import db, Exhibition, Gallery


def insert_kcisa_to_db(data_dict):
    for data in data_dict:
        if data['realmName'] == '미술' :
            id = data['seq']
            title = data['title']
            start_date = datetime.datetime.strptime(data['startDate'], '%Y%m%d').date()
            end_date = datetime.datetime.strptime(data['endDate'], '%Y%m%d').date()
            thumbnail_img = data['thumbnail']
            
            gallery_name = data['place']
            gallery = Gallery.query \
                .filter(Gallery.name==gallery_name) \
                .all()
            if not gallery:
                new_gallery = Gallery(id=str(uuid.uuid4()), name=gallery_name)
                db.session.add(new_gallery)
            gallery = Gallery.query \
                .filter(Gallery.name==gallery_name) \
                .one()
            
            new_exhib = Exhibition(id=id, title=title, start_date=start_date, end_date=end_date,
                                gallery_id=gallery.id, thumbnail_img=thumbnail_img)
            db.session.merge(new_exhib)
    db.session.commit()

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