export function checkin(identity) {
    return {"Packet": "ClientInfo", "HWID": identity};
}
export function pluginRequest(checksum) {
    return {"Packet": "sendPlugin", "Hashes": checksum};
}
export function dispatch(packet) {
    switch (packet["Packet"]) {
        case "savePlugin": return packet["Dll"];
        case "plugin": return packet["Msgpack"];
    }
}
