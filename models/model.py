import datetime

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model) :
    __tablename__ = 'user'
    id = db.Column(db.String(64), primary_key=True)
    email = db.Column(db.String(32))
    nickname = db.Column(db.String(16), nullable=False)
    password = db.Column(db.String(32))
    profile_img = db.Column(db.String(64))
    created_at = db.Column(db.DateTime(), default=datetime.now(), nullable=False)
    gender = db.Column(db.Integer())
    birthdate = db.Column(db.Date())

class Gallery(db.Model):
    __tablename__ = 'gallery'
    id = db.Column(db.String(64), primary_key=True)
    address = db.Column(db.String(128))
    name = db.Column(db.String(32), nullable=False)
    opening_hours = db.Column(db.String())
    description = db.Column(db.String())
    parking_yn = db.Column(db.Boolean())
    contact = db.Column(db.String(32))
    homepage_url = db.Column(db.String(64))
    thumbnail_img = db.Column(db.String(64))

class GalleryOpeningHour(db.Model):
    __tablename__ = 'gallery_opening_hour'
    gallery_id = db.Column(db.String(64), primary_key=True)
    weekday_open_hhmm = db.Column(db.Time())
    weekday_close_hhmm = db.Column(db.Time())
    saturday_open_hhmm = db.Column(db.Time())
    saturday_close_hhmm = db.Column(db.Time())
    holiday_open_hhmm = db.Column(db.Time())
    holiday_close_hhmm = db.Column(db.Time())

class Exhibition(db.Model):
    __tablename__ = 'exhibition'
    id = db.Column(db.String(64), primary_key=True)
    start_date = db.Column(db.Date())
    end_date = db.Column(db.Date())
    title = db.Column(db.String(), nullable=False)
    area = db.Column(db.String())
    gallery_id = db.Column(db.String(64))
    keyword_id = db.Column(db.String(64)) # keyword_id 없이 keyword 테이블에서 primary key 두 개 설정도 고려
    thumbnail_img = db.Column(db.String(64))
    price = db.Column(db.Integer())

class TicketPrice(db.Model):
    __tablename__ = 'ticket_price'
    exhibition_id = db.Column(db.String(64), primary_key=True)
    ticket_type = db.Column(db.Integer(), nullable=False) # Enum 타입도 고려
    final_price = db.Column(db.Integer(), nullable=False)
    available = db.Column(db.Boolean())

class Artist(db.Model):
    __tablename__ = 'artist'
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(16), nullable=False)
    exhibition_id = db.Column(db.String(64))
    thumbnail_img = db.Column(db.String(64))

class Booking(db.Model): # 추후 예매테이블 구체화
    __tablename__ = 'booking'
    id = db.Column(db.String(64), primary_key=True)
    user_id = db.Column(db.String(64), nullable=False)
    gallery_id = db.Column(db.String(64), nullable=False)
    visited_at = db.Column(db.DateTime())

class LikeExhibition(db.Model):
    __tablename__ = 'like_exhibition'
    id = db.Column(db.String(64), primary_key=True)
    user_id = db.Column(db.String(64), nullable=False)
    exhibition_id = db.Column(db.String(64), nullable=False)

class FollowingArtist(db.Model):
    __tablename__ = 'following_artist'
    id = db.Column(db.String(64), primary_key=True)
    user_id = db.Column(db.String(64), nullable=False)
    artist_id = db.Column(db.String(64), nullable=False)

class FollowingGallery(db.Model):
    __tablename__ = 'following_gallery'
    id = db.Column(db.String(64), primary_key=True)
    user_id = db.Column(db.String(64), nullable=False)
    gallery_id = db.Column(db.String(64), nullable=False)

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.String(64), primary_key=True)
    user_id = db.Column(db.String(64), nullable=False)
    exhibition_id = db.Column(db.String(64), nullable=False)
    content = db.Column(db.String())
    created_at = db.Column(db.DateTime(), default=datetime.now(), nullable=False)

class ExhibitionKeyword(db.Model) :
    __tablename__ = 'exhibition_keyword'
    id = db.Column(db.String(64), primary_key=True)
    exhibition_id = db.Column(db.String(64), nullable=False)
    keyword = db.Column(db.String(16), nullable=False)

class ExhibitionArea(db.Model):
    __tablename__ = 'exhibition_area'
    exhibition_id = db.Column(db.String(64), primary_key=True)
    area1 = db.Column(db.String(16))
    area2 = db.Column(db.String(16))
    address = db.Column(db.String(128), nullable=False)

class GalleryCloseDay(db.Model) :
    __tablename__ = 'gallery_close_day'
    gallery_id = db.Column(db.String(64), primary_key=True)
    close_type = db.Column(db.Integer())