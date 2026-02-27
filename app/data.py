import json

class Data:
    def __init__(self) -> None:
        self.separator = ";"

    def data_from_string(self, data_str: str):
        data = data_str.split(self.separator)
        self.data_type = data[0]
        self.payload = data[1]
        self.payload_len = data[2]
        self.device_id = data[3]
        self.mac_addr = data[4]
        self.rssi = data[5]

    def to_json(self) -> dict:
        try:
            parsed_payload = json.loads(self.payload)
        except json.decoder.JSONDecodeError as j:
            print("JSON Error")
            print(f"Payload: \"{self.payload}\"")
            print(f"Error message: {j}")
            parsed_payload = {}

        return {
            "mac_addr": self.mac_addr,
            "data": parsed_payload,
        }
        
