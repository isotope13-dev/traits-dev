fn check(mac: [u8; 6], guest: [u8; 6]) -> Result<(), ()> { if mac == [0; 6] || mac == guest { return Err(()); } Ok(()) }
