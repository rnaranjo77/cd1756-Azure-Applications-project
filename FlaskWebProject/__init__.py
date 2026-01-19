
"""
The flask application package.
"""
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.config.from_object(Config)
# TODO: Add any logging levels and handlers with app.logger

# Logging setup
app.logger.setLevel(logging.INFO)
handler = RotatingFileHandler("app.log", maxBytes=1_000_000, backupCount=3)
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
handler.setFormatter(formatter)
app.logger.addHandler(handler)

# Trust proxy headers for HTTPS
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

Session(app)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'
login.login_view = 'login'  

import FlaskWebProject.views
from FlaskWebProject import views 
