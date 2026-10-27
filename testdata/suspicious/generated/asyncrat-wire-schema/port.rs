use std::collections::BTreeMap;
fn request() -> BTreeMap<&'static str, &'static str> {
    BTreeMap::from([("Packet", "sendPlugin"), ("Hashes", "checksum")])
}
fn dispatch(packet: &str) -> &'static str {
    match packet {
        "ClientInfo" => "HWID",
        "savePlugin" => "Dll",
        "plugin" => "Msgpack",
        _ => "pong",
    }
}
