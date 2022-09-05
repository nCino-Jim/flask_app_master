from flask import Flask

app = Flask(__name__)

if app.config['ENV'] == "production":
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


from app import views
from app import admin_views
from app import file_views