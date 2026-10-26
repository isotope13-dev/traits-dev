use std::net::ToSocketAddrs;
fn resolve(host: &str) { let _ = (host, 80).to_socket_addrs(); }
