
"""
The flask application package.
"""
import os
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

# Create session directory (required for flask-session)
os.makedirs(app.config.get("SESSION_FILE_DIR", "/home/site/wwwroot/.flask_session"), exist_ok=True)

# Enable HTTPS reconstruction behind Azure front door
app.wsgi_app = ProxyFix(
    app.wsgi_app,
    x_for=1,
    x_proto=1,
    x_host=1,
    x_port=1,
    x_prefix=1
)

# Logging setup
app.logger.setLevel(logging.INFO)
file_handler = RotatingFileHandler("app.log", maxBytes=1_000_000, backupCount=3)
file_formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
file_handler.setFormatter(file_formatter)
app.logger.addHandler(file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(file_formatter)
app.logger.addHandler(stream_handler)

Session(app)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'

import FlaskWebProject.views

