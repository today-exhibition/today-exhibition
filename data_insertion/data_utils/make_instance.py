import os
import sys
import uuid

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
from models.model import db, Exhibition, Gallery, GalleryAddress, Artist, ArtistExhibition


def make_gallery_by_name(gallery_name):
    new_gallery = Gallery(id=str(uuid.uuid4()), name=gallery_name)
    db.session.merge(new_gallery)

def make_galleryaddress(gallery_id, area, gpsx, gpsy, address):
    new_gallery_address = GalleryAddress(gallery_id=gallery_id, area=area, gpsx=gpsx, gpsy=gpsy, address=address)
    db.session.merge(new_gallery_address)

def make_exhibition(id, title, start_date, end_date, gallery_id, thumbnail_img):
    new_exhib = Exhibition(id=id, title=title, start_date=start_date, end_date=end_date,
                           gallery_id=gallery_id, thumbnail_img=thumbnail_img)
    db.session.merge(new_exhib)

def make_artist(id, name):
    new_artist = Artist(id=id, name=name)
    db.session.merge(new_artist)

def make_artistexhibition(artist_id, exhibition_id):
    new_artist_exhibition = ArtistExhibition(artist_id=artist_id, exhibition_id=exhibition_id)
    db.session.merge(new_artist_exhibition)