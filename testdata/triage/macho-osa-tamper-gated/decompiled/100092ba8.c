// FUN_100092ba8 @ 100092ba8

/* WARNING: Removing unreachable block (ram,0x000100092db4) */

undefined4 FUN_100092ba8(void)

{
  bool bVar1;
  undefined4 uVar2;
  long unaff_x22;
  uint local_78;
  uint local_74;
  undefined4 local_70;
  undefined4 local_6c;
  undefined4 local_68;
  undefined4 local_64;
  
  local_74 = 0x7d96a0dd;
  local_78 = 0x5d97ae02;
  do {
    if ((int)local_74 < -0x530fa95) {
      if ((int)local_74 < -0x36333092) {
        if (local_74 == 0xa5113fa3) {
          unaff_x22 = (*DAT_1001062f0)(0,0);
          if (unaff_x22 == 0) {
            return 0;
          }
          local_74 = 0x98626a9c;
        }
        else if (local_74 == 0xa6e91364) {
          (*DAT_1001062f8)(unaff_x22,&local_70,FUN_10009e188);
          local_74 = 0x37eb0e78;
        }
        else {
          if (local_74 != 0xc8437660) {
            return 0;
          }
          local_74 = 0xa66800a9;
        }
      }
      else if (local_74 == 0xc9cccf6e) {
        local_70 = 0x3db57053;
        local_74 = 0x7ccb0892;
      }
      else {
        if (local_74 != 0xfa0fc589) {
          uVar2 = 0;
          if (local_74 == 0xd2bffa8f) {
            uVar2 = local_64;
          }
          return uVar2;
        }
        local_74 = 0x6c7a0a4f;
      }
    }
    else if ((int)local_74 < 0x4d30a5cd) {
      if (local_74 == 0xfacf056b) {
        local_74 = 0xb14ce1fe;
      }
      else {
        if (local_74 != 0x48b85a81) {
          return 0;
        }
        local_6c = 0xe621fe9a;
        local_68 = 0x314aebee;
        local_74 = 0x91e8159b;
      }
    }
    else if (local_74 == 0x4d30a5cd) {
      local_64 = 0x276df8ea;
      local_74 = 0xa709141e;
    }
    else if (local_74 == 0x5a4fafb8) {
      if (DAT_1001062f8 == (code *)0x0) {
        DAT_1001062f8 = (code *)FUN_10009b6b4(0xe820e9ec0400a568);
        bVar1 = DAT_1001062f8 == (code *)0x0;
      }
      else {
        bVar1 = false;
      }
      if (DAT_1001062f0 == (code *)0x0) {
        return 0;
      }
      if (bVar1) {
        return 0;
      }
      local_74 = 0x18a60fea;
    }
    else {
      if (local_74 != 0x7d96a0dd) {
        return 0;
      }
      if (DAT_1001062f0 == (code *)0x0) {
        DAT_1001062f0 = (code *)FUN_10009b6b4(0xceb0d6a3ebac423e);
        local_74 = 0x30e63ac1;
      }
      else {
        local_74 = 0x30e63ac1;
      }
    }
    local_78 = local_78 * 0x19660d + 0x3c6ef35f;
    local_74 = local_78 ^ local_74;
  } while( true );
}

