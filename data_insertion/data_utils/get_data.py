import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
from models.model import Gallery, GalleryAddress, Exhibition

def get_gallery_by_name(gallery_name):
    gallery = Gallery.query \
        .filter(Gallery.name==gallery_name) \
        .all()
    return gallery

def get_gallery_id_by_name(gallery_name):
    gallery = Gallery.query \
        .filter(Gallery.name==gallery_name) \
        .one()
    return gallery.id

def get_galleryaddress_by_id(gallery_id):
    gallery_address = GalleryAddress.query \
        .filter(GalleryAddress.gallery_id==gallery_id) \
        .all()
    return gallery_address

def get_exhibition_by_title(exhibition_title):
    exhibition = Exhibition.query \
        .filter(Exhibition.title==exhibition_title) \
        .all()
    return exhibition