import requests, os
from requests.exceptions import RequestException

from ..module_type import ModuleType


class APIService:
    def __init__(self, api_url = os.getenv('COMM_BACKEND_API_URL', "")) -> None:
        self.api_url = api_url

    def post_sensors(self, mac_arg: str, module_type_arg: ModuleType) -> dict:
        api_route = "/sensors"
        print(f"Request {self.api_url} for creating a sensor")
        try:
            result = requests.post(self.api_url + api_route, 
            json={"mac": mac_arg,"module_type": module_type_arg.value}, 
            timeout=1).json()
        except requests.RequestException as re:
            print(f"EXCEPTION: {re}")
            result = {}
        print(result)
        return result
