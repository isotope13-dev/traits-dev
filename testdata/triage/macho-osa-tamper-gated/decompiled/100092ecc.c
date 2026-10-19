// FUN_100092ecc @ 100092ecc

undefined8 FUN_100092ecc(void)

{
  undefined8 uVar1;
  uint local_68;
  uint local_64;
  
  local_64 = 0x3a5325da;
  local_68 = 0xefd2fe02;
  do {
    if ((int)local_64 < 0x2754f7bf) {
      if (local_64 == 0x94bb5976) {
        local_64 = 0x70cc0bd0;
      }
      else {
        if (local_64 != 0xea6a0b96) {
          if (local_64 != 0xd2236fb9) {
            return 0;
          }
          uVar1 = (*DAT_1001061f8)(4);
          return uVar1;
        }
        local_64 = 0xefb44ad7;
      }
    }
    else if (local_64 == 0x2754f7bf) {
      local_64 = 0x380585cd;
    }
    else if (local_64 == 0x3a5325da) {
      local_64 = 0x39b1192;
      if (DAT_1001061f8 == (code *)0x0) {
        if (DAT_100106200 == (code *)0x0) {
          DAT_100106200 = (code *)FUN_10009b6b4(0x89c49442fbc64992);
        }
        local_64 = 0x39b1192;
        DAT_1001061f8 = DAT_100106200;
      }
    }
    else {
      if (local_64 != 0x4a17b4eb) {
        return 0;
      }
      if (DAT_1001061f8 == (code *)0x0) {
        return 0;
      }
      local_64 = 0xf971ff3d;
    }
    local_68 = local_68 * 0x19660d + 0x3c6ef35f;
    local_64 = local_68 ^ local_64;
  } while( true );
}

