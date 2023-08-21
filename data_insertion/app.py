import os
import sys

from flask import Flask

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from config import DEBUG, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from models.model import db

from exhibition_seoul import insert_exhibition_seoul
from exhibition_kcisa import insert_exhibition_kcisa
from gallery_molit import insert_gallery_molit
from user_generator import create_random_user_data, insert_data
from like_exhibition_generator import create_random_likes_data


app = Flask(__name__)

app.instance_path = os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), 'database')
# app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///today-exhibition3.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.debug = DEBUG

db.init_app(app)

@app.route('/')
def main():
    # insert_exhibition_kcisa()
    # insert_gallery_molit()
    insert_exhibition_seoul()
    return "success"

@app.route('/user')
def user():
    #! http://127.0.0.1:8000/user 접속시 dummy user data 생성
    count = 1000
    for _ in range(count):
        # create_random_user_data('print')
        user_data = create_random_user_data()
        insert_data(user_data)
    return ""

@app.route('/likes_exhibition')
def likes():
    #! http://127.0.0.1:8000/user 접속시 dummy likes data 생성
    count = 1000
    for _ in range(count):
        # create_random_user_data('print')
        likes_data = create_random_likes_data()
        db.session.add(likes_data)
    db.session.commit()
    return ""

if __name__ == "__main__" :
    with app.app_context():
        db.create_all()
    app.run(port=8000)