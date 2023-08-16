from flask import Blueprint, render_template, request, redirect, url_for, session
from sqlalchemy import func
from datetime import datetime
from models.model import db, Artist, Exhibition, Gallery, ArtistExhibition, GalleryAddress, User, Comment
import uuid

exhibition_bp = Blueprint('exhibition', __name__)

#! [전시디테일]
@exhibition_bp.route('/exhibition/<id>')
def exhibition(id):
#! [전시디테일 > 전시 정보 조회(전시명, 기간, 시간, 지역, 장소, 요금, 소개, 포스터)]
    exhibition = db.session.query(Exhibition.title,
                                  Exhibition.start_date,
                                  Exhibition.end_date,
                                  Gallery.opening_hours,
                                  GalleryAddress.area,
                                  Gallery.name.label("gallery_name"),
                                  Exhibition.price,
                                  Artist.name.label("artist_name"),
                                  Exhibition.description,
                                  Exhibition.thumbnail_img) \
                .join(Gallery, Exhibition.gallery_id == Gallery.id)\
                .join(GalleryAddress, Gallery.id == GalleryAddress.gallery_id, isouter = True)\
                .join(ArtistExhibition, ArtistExhibition.exhibition_id == Exhibition.id, isouter = True)\
                .join(Artist, Artist.id == ArtistExhibition.artist_id, isouter = True)\
                .filter(Exhibition.id == id).first()

#! [전시디테일 > 전시 코멘트 조회(닉네임, 작성일, 내용)]
    comments = db.session.query(
                User.nickname,
                Comment.content,
                func.substr(Comment.created_at, 1, 10).label("created_at"),
                Comment.id.label("comment_id"),
                Comment.user_id)\
                .join(User, Comment.user_id == User.id)\
                .join(Exhibition, Comment.exhibition_id == Exhibition.id)\
                .filter(Exhibition.id == id).all()

    return render_template('exhibition/exhibition.html', exhibition=exhibition, comments=comments, id=id)

#! [전시디테일 > 전시 코멘트 작성(UUID, 닉네임, 작성일, 내용)]
@exhibition_bp.route('/exhibition/<id>/add_comment', methods=['POST'])
def add_comment(id):
    if "user_id" not in session:
        return render_template("user/login.html")  # /login 페이지로 리다이렉트
    
    user_id = session["user_id"]
    content = request.form['content']
    created_at = datetime.now()

    # Comment 테이블에 새로운 코멘트 추가
    new_comment = Comment(id=str(uuid.uuid4()), user_id=user_id, exhibition_id=id, content=content, created_at=created_at)
    db.session.add(new_comment)
    db.session.commit()

    return redirect(url_for('exhibition.exhibition', id=id))

@exhibition_bp.route('/exhibition/<id>/edit_comment/<comment_id>', methods=['POST'])
def edit_comment(id, comment_id):
    user_id = session.get('user_id')
    edited_content = request.form['edited_content']
    comment = db.session.get(Comment, comment_id)

    if comment:
        comment.content = edited_content
        db.session.commit()

    return redirect(url_for('exhibition.exhibition', id=id))

@exhibition_bp.route('/exhibition/<id>/delete_comment/<comment_id>', methods=['POST'])
def delete_comment(id, comment_id):
    user_id = session.get('user_id')
    comment = db.session.get(Comment, comment_id)

    if comment:        
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('exhibition.exhibition', id=id))