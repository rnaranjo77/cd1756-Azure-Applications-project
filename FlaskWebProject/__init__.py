
"""
The flask application package.
"""
import logging
import os
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.config.from_object(Config)

# TODO: Add any logging levels and handlers with app.logger
# ---- Logging setup (completed) ----
# Determine log level (default to INFO if not provided on Config)
log_level = getattr(Config, "LOG_LEVEL", "INFO")
log_level = logging._nameToLevel.get(str(log_level).upper(), logging.INFO)
app.logger.setLevel(log_level)

# Avoid adding duplicate handlers on reload
if not app.logger.handlers:
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s - %(module)s:%(lineno)d - %(message)s"
    )

    # Stream handler (stdout) for Azure Log Stream / container logs
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(formatter)
    app.logger.addHandler(stream_handler)

    # Rotating file handler (writes to instance/logs/app.log)
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
        # If instance path not available or file system is read-only,
        # fall back to stream-only and record the exception.
        app.logger.warning("File logging disabled: %s", e)

Session(app)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'

import FlaskWebProject.views
