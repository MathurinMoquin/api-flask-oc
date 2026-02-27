import serial, threading, os, time, requests, datetime, subprocess

from .api_service import APIService
from ..module_type import ModuleType
from ..data import Data
from ..mac_table import MACTable

class SerialService:
    def __init__(self, port: str, mact: MACTable, fallback_port: str) -> None:
        self.port = port
        self.last_data = {}
        self.mac_table = mact

        self.data_tag = "DATA: "
        self.discovery_tag = "DISCOVERY: "
        self.api_service = APIService()
        self.discovery_separator = ","
        self.log_file = "/app/log/connection_ESP32.log"

        self.lock = threading.Lock()
        self.stop_event = threading.Event()

        try:
            self.ser = serial.Serial(port, 115200, timeout=0.1)
        except serial.SerialException as se:
            print(se)
            print(f"Serial port {port} not available, is the device not connected or busy?")
            try:
                print(f"Trying with {fallback_port} instead")
                self.ser = serial.Serial(fallback_port, 115200, timeout=0.5)
                self.port = fallback_port
            except serial.SerialException as se:
                print(se)
                print(f"Serial port {fallback_port} not available, is the device not connected or busy?")

    def read_data_continuously(self) -> None:
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

        with open(self.log_file, "a") as f:
            while not self.stop_event.is_set():
                if self.ser == None:
                    try:
                        self.ser = serial.Serial(self.port, 115200, timeout=0.1)
                    except serial.SerialException as se:
                        print(se)
                        print("Serial port not available, is the device not connected or busy?")
                        self.ser = None
                    continue
                try:
                    line = self.ser.readline().decode('utf-8', errors='ignore').strip()
                except serial.SerialException as se:
                    print("Serial port disconnected, retrying in 1 second")
                    print(se)
                    time.sleep(1)
                    continue

                if not line:
                    print("Line is empty")
                    continue

                print(f"Line: {line}")

                if self.discovery_tag in line:
                    data_line = line.split(self.discovery_tag, 1)[1]
                    print(f"New sensor: {data_line}")

                    data = data_line.split(self.discovery_separator)
                    mac = data[0]
                    module_type = ModuleType(data[1])

                    self.create_sensor(mac, module_type)

                elif self.data_tag in line:
                    data_line = line.split(self.data_tag, 1)[1]
                    print(f"New data: {data_line}")
                    
                    data = Data()
                    data.data_from_string(data_line)

                    with self.lock:
                        self.last_data = data.to_json()

                f_data = str(datetime.datetime.now()) + " " + line + '\n'
                f.write(f_data)
                f.flush()

                pass
            pass
        pass

    def create_sensor(self, mac: str, module_type: ModuleType):
        self.api_service.post_sensors(mac, module_type)
        self.mac_table.add_to_table(ModuleType(module_type), mac)
        self.mac_table.save_to_file()
        pass

    def read_data(self) -> dict:
        with self.lock:
            return self.last_data.copy()

    def send_data(self, data: str) -> bool:
        if self.ser == None:
            return False
        try:
            self.ser.write(data.encode('utf-8'))
            self.ser.flush()
            return True
        except serial.SerialException as se:
            print("Cannot send data: ", se)
            return False

    def close_serial_port(self) -> bool:
        if self.ser == None:
            return False
        try:
            self.ser.close()
            return True
        except serial.SerialException as se:
            print("Cannot close the serial port: ", se)
            return False

    def stop(self) -> None:
        self.stop_event.set()
