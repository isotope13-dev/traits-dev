fn transform(input: &[u8], x: u8, y: u8) -> Vec<u8> { input.iter().map(|value| x ^ y).collect() }
