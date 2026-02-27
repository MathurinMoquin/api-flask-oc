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

import sys
sys.stdout.reconfigure(line_buffering=True)


app = create_app()
app.run(host="0.0.0.0", port=5003, debug=True)
