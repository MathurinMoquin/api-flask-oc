from enum import Enum

class FarmCommsMsgTypeT(Enum):
    FARM_COMMS_MSG_REQ_DATA = 1 # Request data from a node
    FARM_COMMS_MSG_DATA     = 2 # Data response
    FARM_COMMS_MSG_CMD      = 3 # Command message
    FARM_COMMS_MSG_ACK      = 4 # Acknowledgement (optional)

