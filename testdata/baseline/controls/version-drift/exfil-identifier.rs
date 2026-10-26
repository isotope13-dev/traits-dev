fn score(text: &str) -> bool { const EXFIL: &[&str] = &["exfiltrate", "upload the"]; EXFIL.iter().any(|s| text.contains(s)) }
