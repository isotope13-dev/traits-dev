fn is_obfuscated_pipeline(cmd: &str) -> bool {
    cmd.contains("| rev |") || cmd.contains("| tr ")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn detects_text_transform_pipelines() {
        assert!(is_obfuscated_pipeline("echo 'lruc' | rev | sh"));
        assert!(is_obfuscated_pipeline("echo 'phey' | tr 'a-za-z' 'n-za-mn-za-m' | sh"));
    }
}
