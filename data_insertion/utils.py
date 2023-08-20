import json
import requests
import xmltodict

def load_secrets():
    with open("../secrets.json", "r") as secrets_file:
        secrets = json.load(secrets_file)
    return secrets

def fetch_api_data(api_url, params=""):
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from the API: {e}")
        return None
    
def fetch_api_data_json(api_url, params=""):
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from the API: {e}")
        return None
    
def convert_xml(xml_data) :
    # xml 데이터가 무조건 있다고 가정
    dict_type = xmltodict.parse(xml_data)
    json_type = json.dumps(dict_type)
    data = json.loads(json_type)
    return data

def get_full_area_name(area) :
    area_dict = {
    '서울': '서울특별시',
    '경기': '경기도',
    '부산': '부산광역시',
    '인천': '인천광역시',
    '강원특별자치도': '강원특별자치도',
    '충남': '충청남도',
    '충북': '충청북도',
    '대구': '대구광역시',
    '대전': '대전광역시',
    '광주': '광주광역시',
    '울산': '울산광역시',
    '전남': '전라남도',
    '전북': '전라북도',
    '경남': '경상남도',
    '경북': '경상북도',
    '제주특별자치도': '제주특별자치도',
    '세종특별자치시': '세종특별자치시'
    }
    if area in area_dict:
        return area_dict[area]
    else:
        return area

def get_address_from_gps(gpsx, gpsy):
    area = None
    address = None
    secrets = load_secrets()
    kakao_api_key = secrets["map"]["kakao_api_key_py"]
    
    url = 'https://dapi.kakao.com/v2/local/geo/coord2address'
    params = {'x': gpsx,
            'y': gpsy,
            'libraries': 'services'}
    header = {'authorization': f'KakaoAK {kakao_api_key}'}
    response = requests.get(url, headers=header, params=params)
    if response.status_code == 200 :
        address = response.json()
        print(address)
        area = address['documents'][0]['address']['region_1depth_name']
        address = address['documents'][0]['address']['address_name']

        area = get_full_area_name(area)
    return area, address