import os
from flask import Flask
from flask_session import Session

from config import DEBUG, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, SECRET_KEY, PORT
from models.model import db

from views.main.main import main_bp
from views.artist.artist import artist_bp
from views.gallery.gallery import gallery_bp
from views.exhibition.exhibition import exhibition_bp
from views.map.map import map_bp
from views.search.search import search_bp
from views.search.search_exhibition import search_exhibition_bp
from views.search.search_artist import search_artist_bp
from views.search.search_gallery import search_gallery_bp
from views.user.user import user_bp
from views.user.exhibition_like import exhibition_like_bp
from views.user.gallery_follow import gallery_follow_bp
from views.user.artist_follow import artist_follow_bp
from views.user.booking_list import booking_list_bp
from views.booking.booking import booking_bp


app = Flask(__name__)

app.secret_key = SECRET_KEY
app.instance_path = os.path.join(os.getcwd(), 'database')
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.debug = True

app.config["SESSION_TYPE"] = "sqlalchemy"
app.config["SESSION_SQLALCHEMY"] = db
Session(app)

db.init_app(app)


app.register_blueprint(main_bp)
app.register_blueprint(artist_bp)
app.register_blueprint(artist_follow_bp)
app.register_blueprint(gallery_bp)
app.register_blueprint(gallery_follow_bp)
app.register_blueprint(exhibition_bp)
app.register_blueprint(exhibition_like_bp)
app.register_blueprint(map_bp)
app.register_blueprint(search_bp)
app.register_blueprint(search_exhibition_bp)
app.register_blueprint(search_artist_bp)
app.register_blueprint(search_gallery_bp)
app.register_blueprint(user_bp)
app.register_blueprint(booking_bp)
app.register_blueprint(booking_list_bp)

if __name__ == "__main__" :
    with app.app_context():
        db.create_all()
    app.run(port=PORT)