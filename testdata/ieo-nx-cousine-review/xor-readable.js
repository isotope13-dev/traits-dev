const checksum = value => (value ^ 0x51 ^ value) + (value ^ 0x62 ^ value) + (value ^ 0x73 ^ value) + (value ^ 0x84 ^ value);
