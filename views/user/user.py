from config import NAVER_CALLBACK_URL, KAKAO_CALLBACK_URL

from flask import Blueprint, render_template, redirect, url_for, session, request, Response
from utils import load_secrets

import requests, datetime, random

from models.model import db, User, LoginType, UserToken
from models.model import UserToken, Booking, LikeExhibition, FollowingArtist, FollowingGallery, Comment
from decorators import check_user_login


user_bp = Blueprint('user', __name__)

# 유저 닉네임 업데이트
def update_user_nickname(user, input_nickname):
    # 유저 닉네임 검증
    if input_nickname == "":
        return "닉네임을 입력해주세요."
    
    if check_duplicate_nickname(input_nickname) == True or user.nickname == input_nickname:
        return "입력한 닉네임은 이미 사용 중이거나 유효하지 않습니다."
    else:
        user.nickname = input_nickname
        db.session.commit()
        
        return "수정되었습니다."

# 유저 데이터 가져오기
def request_user_data(data, social_type) -> User:
    if social_type == "naver":
        account_info = data.get("response")
        
        # response가 없으면 main으로 redirect
        if account_info is None:
            return redirect(url_for('main.main'))
        
        id = account_info.get("id", None)
        email = account_info.get("email", None)
        nickname = account_info.get("nickname", None)
        profile_img = account_info.get("profile_image", None)
        created_at = datetime.datetime.now()
        gender = account_info.get("gender", None)
        if gender is not None:
            gender = "male" if account_info.get("gender") == "M" else "female"
        login_type = LoginType.NAVER
  
    elif social_type == "kakao":
        account_info = data.get("kakao_account")
        
        # response가 없으면 main으로 redirect
        if account_info is None:
            return redirect(url_for('main.main'))
        
        profile = account_info.get("profile")
        
        id = data.get("id", None)
        email = account_info.get("email", None)
        nickname = profile.get("nickname", None)
        profile_img = profile.get("profile_image_url", None)
        created_at = datetime.datetime.now()
        gender = account_info.get("gender", None)
        login_type = LoginType.KAKAO
    
    # social_type이 맞지 않는 경우 예외처리
    else:
        return Response("Bad Request", status=400)
    
    # id를 받지 못한 경우 예외처리
    if id is None:
        return Response("Bad Request", status=400)
    
    user = User(id=id, email=email, nickname=nickname, profile_img=profile_img, \
        created_at=created_at, gender=gender, login_type=login_type)
    
    return user

# 랜덤 닉네임 생성
def generate_random_nickname():
    return ''.join(str(random.randint(0, 9)) for _ in range(16))

# 닉네임 중복 확인
def check_duplicate_nickname(nickname):
    return User.query.filter_by(nickname=nickname).first() is not None

# 신규 유저인 경우 db에 데이터 넣기
def user_signin(user_data: User) -> None:
    user_id = user_data.id
    user = User.query.filter_by(id=user_id).first()
    if not user:
        regist_user = User(
            id = user_data.id,
            email = user_data.email,
            nickname = user_data.nickname,
            profile_img = user_data.profile_img,
            created_at = user_data.created_at,
            gender = user_data.gender,
            login_type = user_data.login_type
        )
        
        # nickname 중복 확인 후 중복이면 random값 부여
        while check_duplicate_nickname(regist_user.nickname):
            random_nickname = generate_random_nickname()
            if not check_duplicate_nickname(random_nickname):
                regist_user.nickname = random_nickname
                break

        db.session.add(regist_user)
        db.session.commit()

# 유저 id 세션에 등록하기
def register_user_id_in_session(id) -> None:
    user_info = db.session.query(User).filter_by(id=id).first()
    if user_info:
        session["user_id"] = user_info.id

def social_signin(data, social_type):
    # 유저 데이터 요청
    user_data = request_user_data(data, social_type)
    # 신규 유저 데이터 등록
    user_signin(user_data)
    # 유저 아이디 세션 등록
    register_user_id_in_session(user_data.id)
    # user_token 테이블에 refresh token 등록
    update_user_refresh_token(data, social_type)
    
    return redirect(url_for('main.main'))

# 유저 리프레쉬 토큰 DB에 등록
def update_user_refresh_token(data, social_type):
    try:
        if social_type == 'naver':
            account_info = data.get('response')
            user_id = account_info.get('id')
            refresh_token = account_info.get('refresh_token')
        if social_type == 'kakao':
            account_info = data.get('kakao_account')
            user_id = data.get('id')
            refresh_token = account_info.get('refresh_token')
    except:
        return redirect(url_for('main.main'))
    
    # DB user_token에 유저 id 있는지 확인 후
    check_user_token = db.session.query(UserToken).filter_by(user_id=user_id).first()
    
    # 유저 아이디가 user_token에 있으면 업데이트 
    if check_user_token:
        check_user_token.refresh_token = refresh_token
    # 유저 아이디가 user_token에 없으면 추가
    if not check_user_token:
        regist_user_token = UserToken(
            user_id = user_id,
            refresh_token = refresh_token
        )
        db.session.add(regist_user_token)
        
    db.session.commit()
    
# update access token
def update_naver_access_token(id, social_keys):
    NAVER_CLIENT_ID = social_keys["naver_client_id"]
    NAVER_CLIENT_SECRET = social_keys["naver_client_secret"]
    
    user_token_info = db.session.query(UserToken).filter_by(user_id=id).first()
    USER_REFRESH_TOKEN = user_token_info.refresh_token
    
    request_update_url = f"https://nid.naver.com/oauth2.0/token?grant_type=refresh_token&client_id={NAVER_CLIENT_ID}&client_secret={NAVER_CLIENT_SECRET}&refresh_token={USER_REFRESH_TOKEN}"
    token_request = requests.get(request_update_url)
    token_json = token_request.json()
    access_token = token_json["access_token"]
    
    return access_token

def update_kakao_access_token(id, social_keys):
    KAKAO_CLIENT_ID = social_keys["kakao_client_id"]
    KAKAO_CLIENT_SECRET = social_keys["kakao_client_id"]
    
    user_token_info = db.session.query(UserToken).filter_by(user_id=id).first()
    USER_REFRESH_TOKEN = user_token_info.refresh_token
    
    request_update_url = f"https://kauth.kakao.com/oauth/token?grant_type=refresh_token&client_id={KAKAO_CLIENT_ID}&client_secret={KAKAO_CLIENT_SECRET}&refresh_token=${USER_REFRESH_TOKEN}"
    token_request = requests.get(request_update_url)
    token_json = token_request.json()
    access_token = token_json["access_token"]
    
    return access_token

def delete_user_related_data(user_id):
    # UserToken, Booking, LikeExhibition, FollowingArtist, FollowingGallery, Comment, User
    db.session.query(UserToken).filter_by(user_id=user_id).delete()
    db.session.query(Booking).filter_by(user_id=user_id).delete()
    db.session.query(LikeExhibition).filter_by(user_id=user_id).delete()
    db.session.query(FollowingArtist).filter_by(user_id=user_id).delete()
    db.session.query(FollowingGallery).filter_by(user_id=user_id).delete()
    db.session.query(Comment).filter_by(user_id=user_id).delete()
    db.session.query(User).filter_by(id=user_id).delete()
    
    db.session.commit()

@user_bp.route('/user', methods=['GET', 'POST'])
@check_user_login
def user():
    user_id = session.get("user_id")
    user = User.query.get(user_id)
    message = None
    
    # 프로필 수정
    if request.method == "POST":
        input_nickname = request.form.get("input_nickname")
        message = update_user_nickname(user, input_nickname)
    
    user_info = db.session.query(
        User.nickname, 
        User.profile_img, 
        User.login_type) \
        .filter_by(id=user_id) \
        .first()
    
    user_info_dict = {
        "nickname": user_info.nickname,
        "profile_img": user_info.profile_img,
        "login_type": user_info.login_type.value,
        "message": message
    }
    
    return render_template("user/user.html", user_info=user_info_dict)

@user_bp.route('/login', methods=['POST'])
def login():
    secrets = load_secrets()
    social_keys = secrets.get("social")
    
    if "naver_login" in request.form:
        NAVER_CLIENT_ID = social_keys["naver_client_id"]
        redirect_request_url = f"https://nid.naver.com/oauth2.0/authorize?client_id={NAVER_CLIENT_ID}&response_type=code&redirect_uri={NAVER_CALLBACK_URL}"
        
        return redirect(redirect_request_url)
    
    elif "kakao_login" in request.form:
        KAKAO_CLIENT_ID = social_keys["kakao_client_id"]
        redirect_request_url = f"https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={KAKAO_CLIENT_ID}&redirect_uri={KAKAO_CALLBACK_URL}"
        
        return redirect(redirect_request_url)
    
    return Response("Bad Request", status=400)

@user_bp.route('/login/callback/naver')
def naver_callback():
    try:
        secrets = load_secrets()
        social_keys = secrets.get("social")
        
        NAVER_CLIENT_ID = social_keys["naver_client_id"]
        NAVER_CLIENT_SECRET = social_keys["naver_client_secret"]
        
        params = request.args.to_dict()
        code = params.get("code")
        request_auth_url = f"https://nid.naver.com/oauth2.0/token?client_id={NAVER_CLIENT_ID}&client_secret={NAVER_CLIENT_SECRET}&grant_type=authorization_code&code={code}"
        
        token_request = requests.get(request_auth_url)
        token_json = token_request.json()
        refresh_token = token_json.get("refresh_token")
        
        ACCESS_TOKEN = token_json.get("access_token", None)
        if ACCESS_TOKEN is None:
            return Response("Unauthorized", status=401)
        
        TOKEN_TYPE = token_json.get("token_type")
        
        profile_request = requests.get(f"https://openapi.naver.com/v1/nid/me", headers={"Authorization": f"{TOKEN_TYPE} {ACCESS_TOKEN}"})
        data = profile_request.json()
        data['response']['refresh_token'] = refresh_token
    except:
        return redirect(url_for('main.main'))
    return social_signin(data, "naver")

@user_bp.route('/login/callback/kakao')
def kakao_callback():
    secrets = load_secrets()
    social_keys = secrets.get("social")
    
    KAKAO_CLIENT_ID = social_keys["kakao_client_id"]
    KAKAO_CLIENT_SECRET = social_keys["kakao_client_id"]
    
    params = request.args.to_dict()
    code = params.get("code")
    request_auth_url = f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={KAKAO_CLIENT_ID}&client_secret={KAKAO_CLIENT_SECRET}&redirect_uri={KAKAO_CALLBACK_URL}&code={code}"
    
    token_request = requests.get(request_auth_url)
    token_json = token_request.json()
    refresh_token = token_json.get("refresh_token")
    
    ACCESS_TOKEN = token_json.get("access_token", None)
    if ACCESS_TOKEN is None:
        return Response("Unauthorized", status=401)
    
    profile_request = requests.get(f"https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})
    data = profile_request.json()
    data['kakao_account']['refresh_token'] = refresh_token
    
    return social_signin(data, "kakao")

@user_bp.route('/logout', methods=['POST'])
def logout():
    if request.method == "POST":
        if "user_id" in session:
            session.clear()
            
    return redirect(url_for('main.main'))

@user_bp.route('/user/delete', methods=['POST'])
def delete():
    secrets = load_secrets()
    social_keys = secrets.get("social")
    user_id = session.get("user_id")
    
    if "naver_delete" in request.form:
        NAVER_CLIENT_ID = social_keys["naver_client_id"]
        NAVER_CLIENT_SECRET = social_keys["naver_client_secret"]
        
        # refresh_token으로 access_token 새롭게 받은 후 delete 진행
        ACCESS_TOKEN = update_naver_access_token(user_id, social_keys)
        request_delete_url = f"https://nid.naver.com/oauth2.0/token?grant_type=delete&client_id={NAVER_CLIENT_ID}&client_secret={NAVER_CLIENT_SECRET}&access_token={ACCESS_TOKEN}&service_provider=NAVER"
        
        delete_request = requests.get(request_delete_url)
        
        # delete request 요청이 성공적인 경우
        if delete_request.json()["result"] == "success":
            # 유저 id로 조회된 컬럼 삭제
            delete_user_related_data(user_id)
            session.clear()
        
    if "kakao_delete" in request.form:
        ACCESS_TOKEN = update_kakao_access_token(user_id, social_keys)
        request_delete_url = f"https://kapi.kakao.com/v1/user/unlink"
        
        delete_request = requests.get(request_delete_url, headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})
        
        if delete_request.json()['id']:
            delete_user_related_data(user_id)
            session.clear()
    
    return redirect(url_for('main.main'))

@user_bp.route('/user/login/check', methods=['POST'])
def login_check():
    if "user_id" not in session:
            return "login_required"
    return "success"