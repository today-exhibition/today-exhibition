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

class DayType(enum.Enum):
    MONDAY = "월요일"
    TUESDAY = "화요일"
    WEDNESDAY = "수요일"
    THURSDAY = "목요일"
    FRIDAY = "금요일"
    SATURDAY = "토요일"
    SUNDAY = "일요일"
    HOLIDAY = "공휴일"

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(64), primary_key=True)
    email = db.Column(db.String(32))
    nickname = db.Column(db.String(16), nullable=False)
    profile_img = db.Column(db.String(64))
    created_at = db.Column(db.DateTime(), default=datetime.datetime.now(), nullable=False)
    gender = db.Column(db.Integer())
    birthdate = db.Column(db.Date())
    login_type = db.Column(db.Enum(LoginType), nullable=False)

class Gallery(db.Model):
    __tablename__ = 'gallery'
    id = db.Column(db.String(64), primary_key=True)
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
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    start_date = db.Column(db.Date())
    end_date = db.Column(db.Date())
    gallery_id = db.Column(db.String(64))
    thumbnail_img = db.Column(db.String(64))
    price = db.Column(db.Integer())

class TicketPrice(db.Model):
    __tablename__ = 'ticket_price'
    exhibition_id = db.Column(db.String(64), primary_key=True)
    ticket_type = db.Column(db.Enum(TicketType), nullable=False)
    final_price = db.Column(db.Integer(), nullable=False)
    available = db.Column(db.Boolean())

class Artist(db.Model):
    __tablename__ = 'artist'
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(16), nullable=False)
    thumbnail_img = db.Column(db.String(64))

class ArtistExhibition(db.Model):
    __tablename__ = 'artist_exhibition'
    artist_id = db.Column(db.String(64), primary_key=True)
    exhibition_id = db.Column(db.String(64), primary_key=True)

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
    liked_at = db.Column(db.DateTime(), default=datetime.datetime.now(), nullable=False)

class FollowingArtist(db.Model):
    __tablename__ = 'following_artist'
    id = db.Column(db.String(64), primary_key=True)
    user_id = db.Column(db.String(64), nullable=False)
    artist_id = db.Column(db.String(64), nullable=False)
    followed_at = db.Column(db.DateTime(), default=datetime.datetime.now(), nullable=False)

class FollowingGallery(db.Model):
    __tablename__ = 'following_gallery'
    id = db.Column(db.String(64), primary_key=True)
    user_id = db.Column(db.String(64), nullable=False)
    gallery_id = db.Column(db.String(64), nullable=False)
    followed_at = db.Column(db.DateTime(), default=datetime.datetime.now(), nullable=False)

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.String(64), primary_key=True)
    user_id = db.Column(db.String(64), nullable=False)
    exhibition_id = db.Column(db.String(64), nullable=False)
    content = db.Column(db.String())
    created_at = db.Column(db.DateTime(), default=datetime.datetime.now(), nullable=False)

class ExhibitionKeyword(db.Model):
    __tablename__ = 'exhibition_keyword'
    exhibition_id = db.Column(db.String(64), primary_key=True)
    keyword = db.Column(db.String(16), primary_key=True)

class GalleryAddress(db.Model):
    __tablename__ = 'gallery_address'
    gallery_id = db.Column(db.String(64), primary_key=True)
    area1 = db.Column(db.String(16))
    area2 = db.Column(db.String(16))
    gpsx = db.Column(db.Float())
    gpsy = db.Column(db.Float())
    address = db.Column(db.String(128), nullable=False)

class GalleryCloseDay(db.Model):
    __tablename__ = 'gallery_close_day'
    gallery_id = db.Column(db.String(64), primary_key=True)
    close_type = db.Column(db.Enum(DayType))
