use std::net::TcpStream;

fn main() {
    // Ordinary build probe: resolves a public hostname, no literal IP,
    // no charset table, no analytics SDK.
    match TcpStream::connect("example.com:80") {
        Ok(_) => println!("cargo:warning=probe ok"),
        Err(_) => println!("cargo:warning=probe failed"),
    }
    println!("cargo:rerun-if-changed=build.rs");
}
