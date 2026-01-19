
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

app = Flask(__name__)
app.config.from_object(Config)

# TODO: Add any logging levels and handlers with app.logger
# ---- Logging setup (completed) ----
# Resolve log level from Config (default to INFO)
log_level_name = str(getattr(Config, "LOG_LEVEL", "INFO")).upper()
log_level = logging._nameToLevel.get(log_level_name, logging.INFO)
app.logger.setLevel(log_level)

# Prevent duplicate handlers (e.g., under reload)
if not app.logger.handlers:
    # Common formatter for both stdout and file
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s - %(module)s:%(lineno)d - %(message)s"
    )

    # Stream handler -> stdout (Azure Log Stream / containers)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(formatter)
    app.logger.addHandler(stream_handler)

    # Optional rotating file handler (graceful if FS is read-only)
    try:
        # Use instance path for write-safe logging directory
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
        # Do not fail app startup due to file logging issues
        app.logger.warning("File logging disabled: %s", e)

# Initialize extensions (order preserved)
Session(app)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'

# Import routes at the end to avoid circular imports
import FlaskWebProject.views  # noqa: E402,F401

