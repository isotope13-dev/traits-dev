fn algorithm(key: &str) -> Option<u8> { match key { "ssh-rsa" => Some(1), _ => None } }
