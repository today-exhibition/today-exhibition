import boto3
import requests
import os

from utils import load_secrets
from config import REGION_NAME, BUCKET_NAME

def thumbnail_to_s3(id, thumbnail_img):
    secrets = load_secrets()
    aws_s3_key = secrets["database"]

    # S3 클라이언트 생성
    s3_client = boto3.client('s3',
        aws_access_key_id = aws_s3_key["aws_s3_Access_key"],
        aws_secret_access_key = aws_s3_key["aws_s3_Secret_access_key"],
        region_name = REGION_NAME
        )

    # 업로드할 이미지 파일과 버킷 이름 설정     
    filename, img_type = image_download(id, thumbnail_img)
    bucket_name = BUCKET_NAME 
    ContentType = get_img_type(img_type.lower())

    # 이미지를 S3 버킷에 업로드 (업로드 위치, 버킷 파일 위치(키))
    s3_client.upload_file(filename, bucket_name, filename, ExtraArgs={'ContentType': ContentType })

    # S3 객체 URL 생성
    object_url = f"https://{bucket_name}.s3.amazonaws.com/{filename}"  
    
    return object_url

def image_download(id, image_url):
    local_directory = 'thumbnail_imgs/'
    response = requests.get(image_url)
    img_type = image_url.split('.')[-1]
    if len(img_type) > 3:
        img_name = f'{id}'
    else:
        img_name = f'{id}.{img_type}'
    file_name = os.path.join(local_directory, img_name)
    
    with open(file_name, 'wb') as f:
        f.write(response.content)
    
    return file_name, img_type

def get_img_type(image_type):
    if image_type == "png":
        ContentType = "image/png"
    elif image_type == "gif":
        ContentType = "image/gif"
    else:
        ContentType = "image/jpeg"
    
    return ContentType