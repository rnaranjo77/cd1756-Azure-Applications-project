
"""
The flask application package.
"""
import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session

# --- Create App ---
app = Flask(__name__)
app.config.from_object(Config)

# --- Trust Azure Reverse Proxy (Fix HTTPS/redirect issues) ---
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# --- Logging Setup (Completed TODO) ---
log_level_name = str(getattr(Config, "LOG_LEVEL", "INFO")).upper()
log_level = logging._nameToLevel.get(log_level_name, logging.INFO)
app.logger.setLevel(log_level)

# Prevent duplicate handlers under debug reload
if not app.logger.handlers:
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s - %(module)s:%(lineno)d - %(message)s"
    )

    # Stream logs (Azure Log Stream)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(formatter)
    app.logger.addHandler(stream_handler)

    # Optional rotating file logs (Azure may restrict FS; handled gracefully)
    try:
        logs_dir = os.path.join(app.instance_path, "logs")
        os.makedirs(logs_dir, exist_ok=True)

        file_handler = RotatingFileHandler(
            os.path.join(logs_dir, "app.log"),
            maxBytes=1_048_576,  # 1 MB
            backupCount=5,
            encoding="utf-8"
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)

    except Exception as e:
        # If FS is read-only, skip file logging
        app.logger.warning("File logging disabled: %s", e)

# --- Flask Extensions ---
Session(app)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'

# Avoid circular import
import FlaskWebProject.views
