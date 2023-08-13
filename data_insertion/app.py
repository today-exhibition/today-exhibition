import os
import sys

from flask import Flask

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from config import DEBUG, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from models.model import db

from exhibition_kcisa import insert_exhibition_kcisa
from gallery_molit import insert_gallery_molit


app = Flask(__name__)

app.instance_path = os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), 'database')
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.debug = DEBUG

db.init_app(app)

@app.route('/')
def main():
    insert_exhibition_kcisa()
    insert_gallery_molit()
    return "success"

if __name__ == "__main__" :
    with app.app_context():
        db.create_all()
    app.run(port=8000)