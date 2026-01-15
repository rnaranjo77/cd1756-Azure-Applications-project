
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

app = Flask(__name__)
app.config.from_object(Config)

# ------------------------------------------
# TODO COMPLETED: Add logging levels & handlers
# ------------------------------------------
app.logger.setLevel(logging.INFO)

# Rotating file handler (local container logs)
file_handler = RotatingFileHandler(
    "app.log", maxBytes=1_000_000, backupCount=3
)
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter(
    "%(asctime)s %(levelname)s %(name)s %(message)s"
)
file_handler.setFormatter(file_formatter)
app.logger.addHandler(file_handler)

# Stream handler (needed for Azure Log Stream visibility)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(file_formatter)
app.logger.addHandler(stream_handler)
# ------------------------------------------

Session(app)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'

import FlaskWebProject.views
