import os
import sys
import uuid
import random
import calendar
import datetime

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from models.model import db, User, Exhibition, LikeExhibition

def create_random_likes_data(output_type=None):
    id = generate_uuid()
    user_id = select_user_id()
    exhibition_id = select_exhibition_id()
    liked_at = generate_liked_at()
    
    new_like = LikeExhibition(id=id, user_id=user_id, exhibition_id=exhibition_id, liked_at=liked_at)
    if output_type == "print":
        n = new_like
        print(n.id, n.user_id, n.exhibition_id, n.liked_at)
    else:
        return new_like
    
def generate_uuid():
    return str(uuid.uuid4())

def generate_liked_at():
    year = random.randint(2022, 2023)
    if year == 2023:
        month = random.randint(1, 8)
    else:
        month = random.randint(1, 12)
    last_day_of_month = calendar.monthrange(year, month)[-1]
    day = random.randint(1, last_day_of_month)

    hour = random.randint(0,23)
    minute = random.randint(0,59)
    second = random.randint(0,59)
    liked_at = datetime.datetime(year, month, day, hour, minute, second)
    return liked_at

def select_user_id():
    users = User.query.all()
    user = random.choice(users)
    return user.id

def select_exhibition_id():
    exhibitions = Exhibition.query.all()
    exhibition = random.choice(exhibitions)
    return exhibition.id
