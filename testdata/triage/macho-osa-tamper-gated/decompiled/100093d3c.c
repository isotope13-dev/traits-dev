// FUN_100093d3c @ 100093d3c

void FUN_100093d3c(undefined8 param_1,undefined8 param_2,long param_3,long param_4)

{
  bool bVar1;
  long lVar2;
  uint local_94;
  uint local_90;
  byte local_89;
  byte local_88 [32];
  long local_68;
  
  local_68 = *(long *)PTR____stack_chk_guard_100102830;
  local_90 = 0x60586322;
  local_94 = 0xf5f1fc3;
  do {
    if ((int)local_90 < 0x3ee1b1d7) {
      if ((int)local_90 < -0xcb2b05e) {
        if (local_90 == 0xbfe9859e) {
          lVar2 = 0;
          do {
            local_89 = local_89 |
                       *(byte *)(param_3 + lVar2) ^ local_88[lVar2] ^ *(byte *)(param_4 + lVar2);
            lVar2 = lVar2 + 1;
          } while (lVar2 != 0x20);
          local_90 = 0xe9e2a0bf;
        }
        else {
          if (local_90 != 0xc0727d40) goto LAB_100093f9c;
          local_90 = 0xc6158bb7;
        }
      }
      else if (local_90 == 0xf34d4fa2) {
        local_89 = 0;
        local_90 = 0xabc7b173;
      }
      else {
        if (local_90 != 0x1c52e63d) goto LAB_100093f9c;
        local_90 = 0xcaf3a271;
      }
    }
    else if ((int)local_90 < 0x6f88bcd9) {
      if (local_90 == 0x3ee1b1d7) {
        local_88[0] = 0;
        local_88[1] = 0;
        local_88[2] = 0;
        local_88[3] = 0;
        local_88[4] = 0;
        local_88[5] = 0;
        local_88[6] = 0;
        local_88[7] = 0;
        local_88[8] = 0;
        local_88[9] = 0;
        local_88[10] = 0;
        local_88[0xb] = 0;
        local_88[0xc] = 0;
        local_88[0xd] = 0;
        local_88[0xe] = 0;
        local_88[0xf] = 0;
        local_88[0x10] = 0;
        local_88[0x11] = 0;
        local_88[0x12] = 0;
        local_88[0x13] = 0;
        local_88[0x14] = 0;
        local_88[0x15] = 0;
        local_88[0x16] = 0;
        local_88[0x17] = 0;
        local_88[0x18] = 0;
        local_88[0x19] = 0;
        local_88[0x1a] = 0;
        local_88[0x1b] = 0;
        local_88[0x1c] = 0;
        local_88[0x1d] = 0;
        local_88[0x1e] = 0;
        local_90 = 0x6b4c7169;
        local_88[0x1f] = 0;
      }
      else {
        if (local_90 != 0x60586322) goto LAB_100093f9c;
        FUN_10009cde8(param_1,param_2,local_88);
        local_90 = 0xf7bb0de4;
      }
    }
    else {
      if (local_90 != 0x6f88bcd9) {
        if (local_90 == 0x78e234ce) {
          bVar1 = local_89 == 0;
          goto LAB_100093fa0;
        }
LAB_100093f9c:
        bVar1 = false;
LAB_100093fa0:
        if (*(long *)PTR____stack_chk_guard_100102830 == local_68) {
          return;
        }
                    /* WARNING: Subroutine does not return */
        ___stack_chk_fail(bVar1);
      }
      local_90 = 0x65b94c86;
    }
    local_94 = local_94 * 0x19660d + 0x3c6ef35f;
    local_90 = local_94 ^ local_90;
  } while( true );
}

