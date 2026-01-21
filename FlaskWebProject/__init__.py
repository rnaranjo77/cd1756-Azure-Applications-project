import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from flask import request, redirect

app = Flask(__name__)

from werkzeug.middleware.proxy_fix import ProxyFix

app.wsgi_app = ProxyFix(
    app.wsgi_app,
    x_proto=1,
    x_host=1
)

app.config.from_object(Config)

@app.before_request
def enforce_https():
    # Trust Azure's X-Forwarded-Proto header
    if request.headers.get('X-Forwarded-Proto', 'http') != 'https' and not app.debug:
        return redirect(request.url.replace("http://", "https://"), code=301)


db = SQLAlchemy(app)

login = LoginManager(app)
login.login_view = 'login'


# ----------------------------
# Logging configuration
# ----------------------------
if not app.debug:
    # Ensure logs are sent to stdout (Azure Log Stream)
    logging.basicConfig(level=logging.INFO)

    file_handler = RotatingFileHandler(
        'app.log',
        maxBytes=10240,
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)

    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Application startup')


from FlaskWebProject import views, models

