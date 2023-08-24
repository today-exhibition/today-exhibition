from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from sqlalchemy import func
from datetime import datetime
from models.model import db, Artist, Exhibition, Gallery, ArtistExhibition, GalleryAddress, User, Comment, LikeExhibition
import uuid

exhibition_bp = Blueprint('exhibition', __name__)


@exhibition_bp.route('/exhibition/<id>')
def exhibition(id):
    # [전시디테일 > 작가 정보 조회]
    artists = db.session.query(
        Artist.id,
        Artist.name)\
        .join(ArtistExhibition, ArtistExhibition.artist_id == Artist.id)\
        .join(Exhibition, Exhibition.id == ArtistExhibition.exhibition_id)\
        .filter(Exhibition.id == id)\
        .all()
    # [전시디테일 > 전시 정보 조회]
    exhibition = db.session.query(
        Exhibition.title,
        Exhibition.start_date,
        Exhibition.end_date,
        Gallery.opening_hours,
        GalleryAddress.area,
        Gallery.id.label("gallery_id"),
        Gallery.name.label("gallery_name"),
        Exhibition.price,
        Artist.name.label("artist_name"),
        Exhibition.description,
        Exhibition.thumbnail_img) \
        .join(Gallery, Exhibition.gallery_id == Gallery.id)\
        .join(GalleryAddress, Gallery.id == GalleryAddress.gallery_id, isouter = True)\
        .join(ArtistExhibition, ArtistExhibition.exhibition_id == Exhibition.id, isouter = True)\
        .join(Artist, Artist.id == ArtistExhibition.artist_id, isouter = True)\
        .filter(Exhibition.id == id) \
        .first()
    # [전시디테일 > 전시 코멘트 조회]
    comments = db.session.query(
        User.nickname,
        Comment.content,
        func.substr(Comment.created_at, 1, 10).label("created_at"),
        Comment.id.label("comment_id"),
        Comment.user_id)\
        .join(User, Comment.user_id == User.id)\
        .join(Exhibition, Comment.exhibition_id == Exhibition.id)\
        .filter(Exhibition.id == id)\
        .all()
    # [전시디테일 > json 형식(작가, 전시, 코멘트)]
    data = {
        "id":id,
        "artists": [
            {"id": artist.id, "name": artist.name} for artist in artists
        ],
        "exhibition": {
            "title": exhibition.title,
            "start_date": exhibition.start_date,
            "end_date": exhibition.end_date,
            "opening_hours": exhibition.opening_hours,
            "area": exhibition.area,
            "gallery_id": exhibition.gallery_id,
            "gallery_name": exhibition.gallery_name,
            "price": exhibition.price,
            "artist_name": exhibition.artist_name,
            "description": exhibition.description,
            "thumbnail_img": exhibition.thumbnail_img
        },
        "comments": [
            {
                "nickname": comment.nickname,
                "content": comment.content,
                "created_at": comment.created_at,
                "comment_id": comment.comment_id,
                "user_id": comment.user_id
            } for comment in comments
        ]
    }

    return render_template('exhibition/exhibition.html', data=data)

# [전시디테일 > 전시 코멘트 작성]
@exhibition_bp.route('/exhibition/<id>/add_comment', methods=['POST'])
def add_comment(id):
    if "user_id" not in session:

        return render_template("user/login.html")  # /login 페이지로 리다이렉트
    
    user_id = session["user_id"]
    content = request.form['content']
    created_at = datetime.now()
    new_comment = Comment(id=str(uuid.uuid4()), user_id=user_id, exhibition_id=id, content=content, created_at=created_at)
    db.session.add(new_comment)
    db.session.commit()

    return redirect(url_for('exhibition.exhibition', id=id))

# [전시디테일 > 전시 코멘트 수정]
@exhibition_bp.route('/exhibition/<id>/edit_comment/<comment_id>', methods=['POST'])
def edit_comment(id, comment_id):
    user_id = session.get('user_id')
    edited_content = request.form['edited_content']
    comment = db.session.get(Comment, comment_id)

    if comment and user_id == comment.user_id:
        comment.content = edited_content
        db.session.commit()

    return redirect(url_for('exhibition.exhibition', id=id))

# [전시디테일 > 전시 코멘트 삭제]
@exhibition_bp.route('/exhibition/<id>/delete_comment/<comment_id>', methods=['POST'])
def delete_comment(id, comment_id):
    user_id = session.get('user_id')
    comment = db.session.get(Comment, comment_id)

    if comment and user_id == comment.user_id:        
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('exhibition.exhibition', id=id))

# [전시디테일 > 전시 좋아요]
@exhibition_bp.route('/exhibition/<exhibition_id>/like', methods=['post'])
def like_exhibition(exhibition_id):
    existing_like = LikeExhibition.query\
        .filter(LikeExhibition.user_id == session["user_id"], LikeExhibition.exhibition_id == exhibition_id)\
        .first()
    
    if existing_like is not None:
        db.session.delete(existing_like)
        db.session.commit()

        return "unliked"
    
    else:
        user_id = session["user_id"]
        liked_at = datetime.now()
        insertdb = LikeExhibition(id=str(uuid.uuid4()), user_id=user_id, exhibition_id=exhibition_id, liked_at=liked_at)
        db.session.add(insertdb)
        db.session.commit()

    return "liked"
