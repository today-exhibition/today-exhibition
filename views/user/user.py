from config import NAVER_CALLBACK_URL, KAKAO_CALLBACK_URL

from flask import Blueprint, render_template, redirect, url_for, session, request, Response
from utils import load_secrets

import requests, datetime, random

from models.model import db, User, LoginType


user_bp = Blueprint('user', __name__)

# 닉네임 검증
def validate_and_update_nickname(user, input_nickname):
    if input_nickname == "":
        return "닉네임을 입력해주세요."
    
    if user.nickname != input_nickname:
        if check_duplicate_nickname(input_nickname) == True:
            return "입력한 닉네임은 이미 사용 중이거나 유효하지 않습니다."

        user.nickname = input_nickname
        db.session.commit()
    return None

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
    user_id = db.session.query(User.id).filter_by(id=id).first()[0]
    if user_id:
        session["user_id"] = user_id

def social_signin(data, social_type):
    # 유저 데이터 요청
    user_data = request_user_data(data, social_type)
    # 신규 유저 데이터 등록
    user_signin(user_data)
    # 유저 아이디 세션 등록
    register_user_id_in_session(user_data.id)
    
    return redirect(url_for('main.main'))


@user_bp.route('/user', methods=['GET', 'POST'])
def user():
    # 로그인 여부 확인
    if not "user_id" in session:
        return render_template("user/login.html")
    
    user_id = session.get("user_id")
    user = User.query.get(user_id)
    
    if request.method == "POST":
        input_nickname = request.form.get("input_nickname")
        error_message = validate_and_update_nickname(user, input_nickname)
        
        if error_message:
            user_info = db.session.query(User.nickname, User.profile_img).filter_by(id=user_id).first()
            return render_template("user/user.html", user_info=user_info, error_message=error_message)
    
    user_info = db.session.query(User.nickname, User.profile_img).filter_by(id=user_id).first()
    
    return render_template("user/user.html", user_info=user_info)

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
        
        ACCESS_TOKEN = token_json.get("access_token", None)
        if ACCESS_TOKEN is None:
            return Response("Unauthorized", status=401)
        TOKEN_TYPE = token_json.get("token_type")
        
        profile_request = requests.get(f"https://openapi.naver.com/v1/nid/me", headers={"Authorization": f"{TOKEN_TYPE} {ACCESS_TOKEN}"})
        data = profile_request.json()
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
    
    ACCESS_TOKEN = token_json.get("access_token", None)
    if ACCESS_TOKEN is None:
        return Response("Unauthorized", status=401)
    
    profile_request = requests.get(f"https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})
    data = profile_request.json()
    
    return social_signin(data, "kakao")

@user_bp.route('/logout', methods=['POST'])
def logout():
    if request.method == "POST":
        if "user_id" in session:
            session.clear()
    return redirect(url_for('main.main'))