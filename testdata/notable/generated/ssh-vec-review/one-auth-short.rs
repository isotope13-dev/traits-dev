use std::net::TcpStream;
use std::io::Read;
use ssh2::Session;

fn main() {
    let tcp = TcpStream::connect("127.0.0.1:2222").unwrap();
    let mut sess = Session::new().unwrap();
    sess.set_tcp_stream(tcp);
    sess.handshake().unwrap();
    
    let overlong = String::from_utf8(vec![b'A'; 256]).unwrap();
    if sess.userauth_password("alpine", &overlong).is_ok() {
        let mut ch = sess.channel_session().unwrap();
        
        let mut s = String::new();
        ch.read_to_string(&mut s).unwrap();
        println!("{}", s);
    }
}
