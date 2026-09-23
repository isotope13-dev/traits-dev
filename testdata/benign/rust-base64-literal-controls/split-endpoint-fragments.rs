//! Split-endpoint fragment test vector.
const PART_A: &str = "aHR0cHM6Ly9teS1hcGk";
const PART_B: &str = "LmV4YW1wbGUuY29tL3Yx";
#[test]
fn fragments_join() {
    assert_eq!(format!("{PART_A}{PART_B}"), "aHR0cHM6Ly9teS1hcGkLmV4YW1wbGUuY29tL3Yx");
}
