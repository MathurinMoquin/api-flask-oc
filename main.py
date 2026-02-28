# from flask import Flask
#
# app = Flask(__name__)
#
# @app.route('/')
# def home():
#     return "Hello"
#
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)
#

from app import create_app
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
import sys, os

sys.stdout.reconfigure(line_buffering=True)

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN", ""),
    integrations=[FlaskIntegration()],
    traces_sample_rate=0.0,
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
)

app = create_app()
app.run(host="0.0.0.0", port=5003, debug=False)
