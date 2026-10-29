use std::{fs, path::Path};
fn clean(home: &Path) { let _ = fs::remove_dir_all(home); }
fn main() { let home = dirs::home_dir().unwrap().join(".sample").join("cache"); clean(&home); }
