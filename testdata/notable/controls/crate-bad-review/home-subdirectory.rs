use std::fs;
fn main() {
    let home = dirs::home_dir().unwrap().join(".sample");
    fs::remove_dir_all(&home);
}
