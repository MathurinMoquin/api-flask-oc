import time
from .mac_table import MACTable
from .module_type import ModuleType
from .services.serial_service import SerialService
from .farm_comms_msg_type_t import FarmCommsMsgTypeT

class RouteData:
    def __init__(self, sc: SerialService, mact: MACTable) -> None:
        self.serial_comm = sc
        self.mac_table = mact
        self.time_between_send_and_read = 0.07
        pass

    def get_all_from_module(self, module_type: ModuleType) -> dict:
        d = {}

        print(f"Calling all {module_type.value}")
        for module in self.mac_table.table[module_type.value]:
            print(f'Requesting data from: {module["mac"]}')
            d[module["mac"]] = self.send_command(module["mac"])

        return d

    def post_change_valves(self, mac: str, new_state: int) -> dict:
        module_type = ModuleType.WATER_FLOW
        d = {}

        for module in self.mac_table.table[module_type.value]:
            if module["mac"] != mac:
                return { "status": "error", "message": f"no device with mac address: {mac}" }

        self.send_command(mac, FarmCommsMsgTypeT.FARM_COMMS_MSG_CMD.value)
        time.sleep(0.5)
        data = self.send_command(mac)

        return { "status": "ok", "data": data }

    def send_command(self, mac_addr: str, demand_type = 1, msg = "", middle_delimiter = ',', end_limiter = '|') -> dict:
        cmd = mac_addr + middle_delimiter + str(demand_type) + middle_delimiter + msg + end_limiter
        self.serial_comm.send_data(cmd)
        time.sleep(self.time_between_send_and_read)
        d = self.serial_comm.read_data()
        return d
