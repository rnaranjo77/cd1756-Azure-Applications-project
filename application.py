"""
This script runs the FlaskWebProject application using a development server.
"""

from os import environ
from FlaskWebProject import app

if __name__ == '__main__':
    # Azure provides PORT; fallback to 5555 for local dev
    PORT = int(environ.get("PORT", 5555))

    # MUST bind to 0.0.0.0 on Azure
    HOST = "0.0.0.0"

    # Do NOT use ssl_context on Azure (TLS is terminated by App Service)
    app.run(host=HOST, port=PORT)
``

