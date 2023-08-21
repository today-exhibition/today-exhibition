import os
import sys
import uuid
import string
import random
import datetime

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from models.model import db, User


letters_set = string.ascii_letters
digits_set = string.digits

# type -> print, insert_db
def create_random_user_data(output_type=None):
    id = generate_uuid()
    email = generate_email()
    nickname = generate_nickname()
    created_at = generate_created_at()
    gender = generate_gender_type()
    login_type = generate_user_login_type()
    
    new_user = User(id=id, email=email, nickname=nickname, created_at=created_at, gender=gender, login_type=login_type)
    if output_type == "print":
        n = new_user
        print(n.id, n.email, n.nickname, n.created_at, n.gender, n.login_type)
    else:
        return new_user

def generate_uuid():
    return str(uuid.uuid4())

def generate_email():
    if random.choice([True, False]):
        id_len = random.randint(10, 20)
        mail_len = random.randint(10, 20)
        id = ''.join([random.choice(letters_set+digits_set) for i in range(id_len)])
        mail = ''.join([random.choice(letters_set+digits_set) for i in range(mail_len)])
        return id+'@'+mail
    
def generate_nickname():
    nickname_len = random.randint(5, 15)
    nickname = ''.join([random.choice(letters_set+digits_set) for i in range(nickname_len)])
    return nickname

def generate_created_at():
    mdays = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    year = random.randint(2022, 2023)
    if year == 2023:
        month = random.randint(1, 8)
    else:
        month = random.randint(1, 12)
    
    if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
        mdays[2] = 29
        
    day = random.randint(1, mdays[month])
    hour = random.randint(0,23)
    minute = random.randint(0,59)
    second = random.randint(0,59)
    order_at = datetime.datetime(year, month, day, hour, minute, second)
    return order_at

def generate_gender_type():
    if random.choice([True, False]):
        return random.choice(["male", "female"])

def generate_user_login_type():
    return random.choice(["NAVER", "KAKAO"])

def insert_data(user):
    db.session.add(user)
    db.session.commit()

if __name__ == '__main__':
    count = int(input('생성할 유저 개수를 정해주세요: '))
    for _ in range(count):
        create_random_user_data('print')