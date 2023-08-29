from flask import Blueprint, render_template, request, redirect, url_for, session
from sqlalchemy import func
from datetime import datetime
from models.model import db, Artist, Exhibition, Gallery, ArtistExhibition, GalleryAddress, User, Comment, LikeExhibition
from views.artist.artist import get_artist_data
from views.search.search import get_liked_exhibition_ids
import uuid
from decorators import check_user_login


exhibition_bp = Blueprint('exhibition', __name__)

# 전시 디테일 (작가, 전시, 코멘트, 전시좋아요)
@exhibition_bp.route('/exhibition/<id>')
def exhibition(id):
    artists = get_artist_data(id)\
        .join(ArtistExhibition, ArtistExhibition.artist_id == Artist.id)\
        .join(Exhibition, Exhibition.id == ArtistExhibition.exhibition_id)\
        .filter(Exhibition.id == id)\
        .all()
    exhibition = get_exhibition_data(id)
    comments = get_comments_data(id)

    user_id = session.get('user_id', None)
    liked_exhibition_ids = get_liked_exhibition_ids(user_id)

    data =  {
        "id": id,
        "artists": artists,
        "exhibition": exhibition,
        "comments": comments,
        "user_id": user_id,
        "liked_exhibition_ids": liked_exhibition_ids
        }
    
    return render_template('exhibition/exhibition.html', data=data)

# 전시 코멘트 작성
@exhibition_bp.route('/exhibition/<id>/add_comment', methods=['POST'])
@check_user_login
def add_comment(id):
    user_id = session["user_id"]
    content = request.form['content']
    created_at = datetime.now()
    new_comment = Comment(id=str(uuid.uuid4()), user_id=user_id, exhibition_id=id, content=content, created_at=created_at)
    db.session.add(new_comment)
    db.session.commit()

    return redirect(url_for('exhibition.exhibition', id=id))

# 전시 코멘트 수정
@exhibition_bp.route('/exhibition/<id>/edit_comment/<comment_id>', methods=['POST'])
def edit_comment(id, comment_id):
    user_id = session.get('user_id')
    edited_content = request.form['edited_content']
    comment = db.session.get(Comment, comment_id)

    if comment and user_id == comment.user_id:
        comment.content = edited_content
        db.session.commit()

    return redirect(url_for('exhibition.exhibition', id=id))

# 전시 코멘트 삭제
@exhibition_bp.route('/exhibition/<id>/delete_comment/<comment_id>', methods=['POST'])
def delete_comment(id, comment_id):
    user_id = session.get('user_id')
    comment = db.session.get(Comment, comment_id)

    if comment and user_id == comment.user_id:        
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('exhibition.exhibition', id=id))

# [함수] 전시
def get_exhibition_data(id):
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
    
    return exhibition
    
# [함수] 코멘트
def get_comments_data(id):
    comments = db.session.query(
        User.nickname,
        Comment.content,
        func.substr(Comment.created_at, 1, 10).label("created_at"),
        Comment.id.label("comment_id"),
        Comment.user_id)\
        .join(User, Comment.user_id == User.id)\
        .join(Exhibition, Comment.exhibition_id == Exhibition.id)\
        .filter(Exhibition.id == id)\
        .order_by(Comment.created_at.desc())\
        .all()
    
    return comments

# 전시 좋아요
@exhibition_bp.route('/exhibition/<exhibition_id>/like', methods=['post'])
def like_exhibition(exhibition_id):
    existing_like = LikeExhibition.query \
        .filter(LikeExhibition.user_id == session["user_id"], LikeExhibition.exhibition_id == exhibition_id) \
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
