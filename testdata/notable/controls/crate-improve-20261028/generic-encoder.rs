fn encode(data: &[u8], key: &[u8]) -> Vec<u8> { data.iter().enumerate().map(|(offset, byte)| byte ^ key[offset % key.len()]).collect() }
