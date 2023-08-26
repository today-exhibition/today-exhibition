import datetime
import enum

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class LoginType(enum.Enum):
    NAVER = "NAVER"
    KAKAO = "KAKAO"

class TicketType(enum.Enum):
    NO_DISCOUNT = 0
    STUDENT = 1
    SENIOR_CITIZEN = 2
    GROUP = 3
    EARLY_BIRD = 4

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(64), primary_key=True)
    email = db.Column(db.String(32))
    nickname = db.Column(db.String(16), nullable=False)
    profile_img = db.Column(db.String(256))
    created_at = db.Column(db.DateTime(), default=datetime.datetime.now(), nullable=False)
    gender = db.Column(db.String(6))
    login_type = db.Column(db.Enum(LoginType), nullable=False)

    user_token_R = db.relationship('UserToken', backref='user')
    booking_R = db.relationship('Booking', backref='user')
    like_exhibition_R = db.relationship('LikeExhibition', backref='user')
    following_artist_R = db.relationship('FollowingArtist', backref='user')
    following_gallery_R = db.relationship('FollowingGallery', backref='user')
    comment_R = db.relationship('Comment', backref='user')

class UserToken(db.Model):
    __tablename__ = 'user_token'
    user_id = db.Column(db.String(64), db.ForeignKey('user.id'), primary_key=True)
    refresh_token = db.Column(db.String())

class Gallery(db.Model):
    __tablename__ = 'gallery'
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    opening_hours = db.Column(db.String())
    holiday_info = db.Column(db.String(128))
    description = db.Column(db.String())
    parking_yn = db.Column(db.Boolean())
    contact = db.Column(db.String(32))
    homepage_url = db.Column(db.String(64))
    thumbnail_img = db.Column(db.String(256))

    gallery_address_R = db.relationship('GalleryAddress', backref='gallery')
    gallery_opening_hour_R = db.relationship('GalleryOpeningHour', backref='gallery')
    exhibition_R = db.relationship('Exhibition', backref='gallery')
    following_gallery_R = db.relationship('FollowingGallery', backref='gallery')

class GalleryAddress(db.Model):
    __tablename__ = 'gallery_address'
    gallery_id = db.Column(db.String(64), db.ForeignKey('gallery.id'), primary_key=True)
    area = db.Column(db.String(16))
    gpsx = db.Column(db.Float())
    gpsy = db.Column(db.Float())
    address = db.Column(db.String(128), nullable=False)

class GalleryOpeningHour(db.Model):
    __tablename__ = 'gallery_opening_hour'
    gallery_id = db.Column(db.String(64), db.ForeignKey('gallery.id'), primary_key=True)
    weekday_open_hhmm = db.Column(db.Time())
    weekday_close_hhmm = db.Column(db.Time())
    saturday_open_hhmm = db.Column(db.Time())
    saturday_close_hhmm = db.Column(db.Time())
    holiday_open_hhmm = db.Column(db.Time())
    holiday_close_hhmm = db.Column(db.Time())

class Exhibition(db.Model):
    __tablename__ = 'exhibition'
    id = db.Column(db.String(64), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    start_date = db.Column(db.Date())
    end_date = db.Column(db.Date())
    gallery_id = db.Column(db.String(64), db.ForeignKey('gallery.id'))
    thumbnail_img = db.Column(db.String(256))
    price = db.Column(db.Integer())

    exhibition_keyword_R = db.relationship('ExhibitionKeyword', backref='exhibition')
    ticket_price_R = db.relationship('TicketPrice', backref='exhibition')
    artist_exhibition_R = db.relationship('ArtistExhibition', backref='exhibition')
    booking_R = db.relationship('Booking', backref='exhibition')
    like_exhibition_R = db.relationship('LikeExhibition', backref='exhibition')
    comment_R = db.relationship('Comment', backref='exhibition')

class ExhibitionKeyword(db.Model):
    __tablename__ = 'exhibition_keyword'
    exhibition_id = db.Column(db.String(64), db.ForeignKey('exhibition.id'), primary_key=True)
    keyword = db.Column(db.String(16), primary_key=True)

class TicketPrice(db.Model):
    __tablename__ = 'ticket_price'
    exhibition_id = db.Column(db.String(64), db.ForeignKey('exhibition.id'), primary_key=True)
    ticket_type = db.Column(db.Enum(TicketType), nullable=False)
    final_price = db.Column(db.Integer(), nullable=False)
    available = db.Column(db.Boolean())

class Artist(db.Model):
    __tablename__ = 'artist'
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(16), nullable=False)
    thumbnail_img = db.Column(db.String(256))

class ArtistExhibition(db.Model):
    __tablename__ = 'artist_exhibition'
    artist_id = db.Column(db.String(64), db.ForeignKey('artist.id'), primary_key=True)
    exhibition_id = db.Column(db.String(64), db.ForeignKey('exhibition.id'), primary_key=True)

class Booking(db.Model): # 추후 예매테이블 구체화
    __tablename__ = 'booking'
    id = db.Column(db.String(64), primary_key=True)
    user_id = db.Column(db.String(64), db.ForeignKey('user.id'), nullable=False)
    exhibition_id = db.Column(db.String(64), db.ForeignKey('exhibition.id'), nullable=False)
    visited_at = db.Column(db.DateTime())

class LikeExhibition(db.Model):
    __tablename__ = 'like_exhibition'
    id = db.Column(db.String(64), primary_key=True)
    user_id = db.Column(db.String(64), db.ForeignKey('user.id'), nullable=False)
    exhibition_id = db.Column(db.String(64), db.ForeignKey('exhibition.id'), nullable=False)
    liked_at = db.Column(db.DateTime(), default=datetime.datetime.now(), nullable=False)

class FollowingArtist(db.Model):
    __tablename__ = 'following_artist'
    id = db.Column(db.String(64), primary_key=True)
    user_id = db.Column(db.String(64), db.ForeignKey('user.id'), nullable=False)
    artist_id = db.Column(db.String(64), db.ForeignKey('artist.id'), nullable=False)
    followed_at = db.Column(db.DateTime(), default=datetime.datetime.now(), nullable=False)

class FollowingGallery(db.Model):
    __tablename__ = 'following_gallery'
    id = db.Column(db.String(64), primary_key=True)
    user_id = db.Column(db.String(64), db.ForeignKey('user.id'), nullable=False)
    gallery_id = db.Column(db.String(64), db.ForeignKey('gallery.id'), nullable=False)
    followed_at = db.Column(db.DateTime(), default=datetime.datetime.now(), nullable=False)

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.String(64), primary_key=True)
    user_id = db.Column(db.String(64), db.ForeignKey('user.id'), nullable=False)
    exhibition_id = db.Column(db.String(64), db.ForeignKey('exhibition.id'), nullable=False)
    content = db.Column(db.String())
    created_at = db.Column(db.DateTime(), default=datetime.datetime.now(), nullable=False)
