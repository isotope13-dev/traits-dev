def dispatch(packet):
    if packet["Packet"] == "savePlugin":
        return packet["Dll"]
    if packet["Packet"] == "plugin":
        return packet["Msgpack"]

def request(checksum):
    return {"Packet": "sendPlugin", "Hashes": checksum}
