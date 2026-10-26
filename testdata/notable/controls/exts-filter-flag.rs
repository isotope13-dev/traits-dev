//! Diff-equivalence oracle options:
//!   --exts .ts,.tsx    extensions a commit must touch to qualify
//!   --commits N        how many qualifying commits to replay
fn parse_exts(raw: &str) -> Vec<String> {
    raw.split(',').map(|s| s.trim().to_ascii_lowercase()).collect()
}
