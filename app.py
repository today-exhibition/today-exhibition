from flask import Flask

from models.model import db

from views.search.search import search_bp


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///today-exhibition.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.debug = True

db.init_app(app)

app.register_blueprint(search_bp)


if __name__ == "__main__" :
    with app.app_context():
        db.create_all()
    app.run()