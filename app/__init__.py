from flask import Flask

app = Flask(__name__)

if app.config['ENV'] == "PROD":
    app.config.from_object("config.ProdConfig")
else:
    app.config.from_object("config.DevConfig")





from app import views
from app import admin_views
from app import file_views

from app import itunes_views