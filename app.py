import os
from flask import Flask

from config import DEBUG, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from models.model import db

from views.map.map import map_bp

app = Flask(__name__)

app.instance_path = os.path.join(os.getcwd(), 'database')
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.debug = DEBUG

db.init_app(app)

app.register_blueprint(map_bp)

if __name__ == "__main__" :
    with app.app_context():
        db.create_all()
    app.run(port=8000)