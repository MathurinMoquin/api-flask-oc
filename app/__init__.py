import sys, signal, os
from threading import Thread
from flask import Flask
from flask_cors import CORS

from app.mac_table import MACTable
from app.services.serial_service import SerialService

mact = MACTable()
ss = SerialService("/dev/ttyUSB0", mact, "/dev/ttyUSB1")

thread = Thread(target=ss.read_data_continuously, args=())
thread.start()

def shutdown_handler(sig, frame):
    print("\nStopping thread...")
    ss.stop()
    thread.join()
    print("Clean exit")
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_handler)

def create_app():
    app = Flask(__name__)
    url = os.getenv('COMM_BACKEND_API_URL', '')
    CORS(app, origins=[url])
    # CORS(app, origins=["*"])

    from .routes import main
    app.register_blueprint(main)

    return app
