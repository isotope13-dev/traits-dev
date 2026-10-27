def checkin(identity):
    return {"Packet": "ClientInfo", "HWID": identity}

def plugin_request(checksum):
    return {"Packet": "sendPlugin", "Hashes": checksum}

def dispatch(packet):
    if packet["Packet"] == "savePlugin":
        return packet["Dll"]
    if packet["Packet"] == "plugin":
        return packet["Msgpack"]
