import os, json
from .module_type import ModuleType

class MACTable:
    def __init__(self) -> None:
        self.file_name = "mac_table.json"

        if os.path.exists(self.file_name):
            self.get_from_file()
            pass
        else:
            self.table = {
                ModuleType.POULAILLER.value: [],
                ModuleType.FRIGO.value: [],
                ModuleType.WATER_FLOW.value: [],
            }

        print(self.table)

    def add_to_table(self, module_type: ModuleType, mac_addr: str) -> bool:
        entry = {
            "mac": mac_addr
        }
        
        key = module_type.value

        if key not in self.table:
            print(f"ARGGGGG: {key}, TABLE: {self.table}")
            self.table[key] = []

        for sensor in self.table[key]:
            if sensor["mac"] == mac_addr:
                return False

        self.table[key].append(entry)
        return True

    def delete_from_table(self, mac: str) -> bool:
        for module_type in self.table:
            for module in self.table[module_type]:
                if module["mac"] == mac:
                    self.table[module_type].remove(module)
                    return True

        return False
    
    def save_to_file(self) -> None:
        os.makedirs(os.path.dirname("./" + self.file_name), exist_ok=True)

        with open(self.file_name, "w") as f:
            json.dump(self.table, f, indent=4)

    def get_from_file(self) -> None:
        if not os.path.exists(self.file_name):
            return

        with open(self.file_name, "r") as f:
            lines = f.readlines()
            data = "".join(lines)
            parsed_json_data = json.loads(data)
            self.table = parsed_json_data
