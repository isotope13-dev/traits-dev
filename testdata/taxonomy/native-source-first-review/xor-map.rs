fn transform(input: &[u8], key: u8) -> Vec<u8> { input.iter().map(|value| value ^ key).collect() }
