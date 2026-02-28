
from flask import Blueprint, request
from .module_type import ModuleType
from .routes_data import RouteData

from app import ss, mact

main = Blueprint("main", __name__)

rd = RouteData(ss, mact)

@main.get("/poulaillers")
def get_poulaillers():
    return rd.get_all_from_module(ModuleType.POULAILLER)

@main.get("/frigos")
def get_frigos():
    x={}
    print(x["frigos"])
    return rd.get_all_from_module(ModuleType.FRIGO)

@main.get("/water_flows")
def get_water_flows():
    return rd.get_all_from_module(ModuleType.WATER_FLOW)

@main.post("/valves")
def post_valves():
    mac = request.values.get('mac')
    new_state = request.values.get('new_state')

    if mac == None:
        return {"error": "mac address is null"}
    if new_state == None:
        return {"error": "new_state is null"}
    
    if new_state != 1 and new_state != 0:
        return {"error": "new_state can only be 1 or 0"}
    return rd.post_change_valves(mac, int(new_state))
    
