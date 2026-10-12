fn main() {
    let key = r"HKCU\Software\Microsoft\Windows\CurrentVersion\Run";
    let name = "SecurityUpdate";
    let value_type = "REG_SZ";
    println!("{key} {name} {value_type}");
}
