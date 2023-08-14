from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy import func
from datetime import datetime
from models.model import db, Artist, Exhibition, Gallery, ArtistExhibition, GalleryAddress, User, Comment
import uuid

exhibition_bp = Blueprint('exhibition', __name__)

#! [전시디테일]
@exhibition_bp.route('/exhibition/<id>')
def exhibition(id):
#! [전시디테일 > 전시 정보 조회(전시명, 기간, 시간, 지역, 장소, 요금, 소개, 포스터)]
    exhibitions = db.session.query(
                Exhibition.title,  
                Exhibition.start_date, 
                Exhibition.end_date,
                Gallery.opening_hours,
                GalleryAddress.area,
                Gallery.name,
                Exhibition.price,
                Artist.name,
                Exhibition.description,
                Exhibition.thumbnail_img)\
                .join(Gallery, Exhibition.gallery_id == Gallery.id)\
                .join(GalleryAddress, Gallery.id == GalleryAddress.gallery_id)\
                .join(ArtistExhibition, ArtistExhibition.exhibition_id == Exhibition.id)\
                .join(Artist, Artist.id == ArtistExhibition.artist_id)\
                .filter(Exhibition.id == id).all()
#! [전시디테일 > 전시 코멘트 조회(닉네임, 작성일, 내용)]
    comments = db.session.query(
                User.id,
                Comment.content,
                func.substr(Comment.created_at, 1, 10),
                Comment.id)\
                .join(User, Comment.user_id == User.id)\
                .join(Exhibition, Comment.exhibition_id == Exhibition.id)\
                .filter(Exhibition.id == id).all()
    print(comments)

    return render_template('exhibition/exhibition.html', exhibitions=exhibitions, comments=comments, id=id)

#! [전시디테일 > 전시 코멘트 작성(UUID, 닉네임, 작성일, 내용)]
@exhibition_bp.route('/exhibition/<id>/add_comment', methods=['POST'])
def add_comment(id):
    # 이용자 아이디는 무조건 1로 설정 -> 세션에서 이용자 ID 가져오도록 변경   
    user_id = 1 #session.get('user_id')
    content = request.form['content']
    created_at = datetime.now()

    # Comment 테이블에 새로운 코멘트 추가
    new_comment = Comment(id=str(uuid.uuid4()), user_id=user_id, exhibition_id=id, content=content, created_at=created_at)
    db.session.add(new_comment)
    db.session.commit()
    print(new_comment)

    return redirect(url_for('exhibition.exhibition', id=id))

@exhibition_bp.route('/exhibition/<id>/edit_comment/<comment_id>', methods=['POST'])
def edit_comment(id, comment_id):
    edited_content = request.form['edited_content']

    comment = db.session.get(Comment, comment_id) #Comment.query.get(comment_id)
    if comment:
        comment.content = edited_content
        db.session.commit()

    return redirect(url_for('exhibition.exhibition', id=id))

@exhibition_bp.route('/exhibition/<id>/delete_comment/<comment_id>', methods=['POST'])
def delete_comment(id, comment_id):
    # user_id = session.get('user_id')  # 세션에서 사용자 ID 가져오도록 변경
    comment = db.session.get(Comment, comment_id) #query.get(comment_id)
    if comment: # comment and comment.user_id == user_id:   해당 코멘트의 작성자와 현재 로그인된 이용자가 동일한지 체크
        db.session.commit()
        db.session.delete(comment)

    return redirect(url_for('exhibition.exhibition', id=id))