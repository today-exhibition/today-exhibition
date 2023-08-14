from flask import Blueprint, render_template, session

from models.model import db, User


main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def main():
    if "user_id" in session:
        user_id = session.get("user_id")
        login_user_id = db.session.query(User.id).filter_by(id=user_id).first()[0]
        return render_template('main/main.html', user_id=login_user_id)    
    return render_template('main/main.html')