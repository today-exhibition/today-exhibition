import json
import requests
import xmltodict

def load_secrets():
    with open("../secrets.json", "r") as secrets_file:
        secrets = json.load(secrets_file)
    return secrets

def fetch_api_data(api_url, params):
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from the API: {e}")
        return None
    
def convert_xml(xml_data) :
    # xml 데이터가 무조건 있다고 가정
    dict_type = xmltodict.parse(xml_data)
    json_type = json.dumps(dict_type)
    data = json.loads(json_type)
    return data