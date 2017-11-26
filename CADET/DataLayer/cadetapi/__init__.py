""" This is the root file for the web server. It instantiates the important
    extensions and ties them to the Flask 'app' object.
    More information can be found at the following:
    http://flask.pocoo.org/docs/0.12/
"""

from flask import Flask, redirect, url_for
from .config import DevConfig, MysqlConfig

from .models import db
from .schemas import ma
from .urls import rest_api

# create app using a config
app = Flask(__name__)
app.config.from_object(DevConfig)
#app.config.from_object(MysqlConfig)

# link sqlalchemy db to the app
db.init_app(app)
ma.init_app(app)

#initialize the database if necessary
app.app_context().push()
db.create_all()

# link restful api to the app
rest_api.init_app(app)


# Test route: currently no need for it. consider for future deletion
@app.route('/hello')
@app.route('/')
def index():
    return "Hello, World"

if __name__ == "__main__":
#    app = create_app()
    app.run()
