// FUN_10009c1c0 @ 10009c1c0

ulong FUN_10009c1c0(long *param_1,byte *param_2)

{
  bool bVar1;
  ulong uVar2;
  byte *pbVar3;
  byte *pbVar4;
  ulong uVar5;
  uint local_8;
  uint local_4;
  
  uVar5 = 0;
  local_4 = 0xfb2d981f;
  uVar2 = 0x11fbba9a;
  local_8 = 0x11fbba9a;
  pbVar3 = (byte *)*param_1;
  do {
    while( true ) {
      while (local_4 == 0xbc0de628) {
        local_8 = local_8 * 0x19660d + 0x3c6ef35f;
        local_4 = local_8 ^ 0x40924c70;
      }
      if ((int)local_4 < 0x216a498d) break;
      if (local_4 == 0x216a498d) {
        return uVar2;
      }
      if (local_4 != 0x4513f077) {
        return 0;
      }
      uVar5 = 0;
      local_8 = local_8 * 0x19660d + 0x3c6ef35f;
      local_4 = local_8 ^ 0xb0f062bd;
    }
    if (local_4 == 0xf5cdd261) {
      if ((param_2 <= pbVar3) || (pbVar4 = pbVar3, 0x3f < uVar5)) {
LAB_10009c324:
        *param_1 = (long)(param_2 + 1);
        return 0;
      }
      while( true ) {
        pbVar3 = pbVar4 + 1;
        *param_1 = (long)pbVar3;
        uVar2 = ((ulong)*pbVar4 & 0x7f) << (uVar5 & 0x3f) | uVar2;
        if (-1 < (char)*pbVar4) break;
        if ((param_2 <= pbVar3) || (bVar1 = 0x38 < uVar5, uVar5 = uVar5 + 7, pbVar4 = pbVar3, bVar1)
           ) goto LAB_10009c324;
      }
      uVar5 = (ulong)((int)uVar5 + 7);
      local_4 = 0xbbeedf06;
    }
    else {
      if (local_4 != 0xfb2d981f) {
        return 0;
      }
      uVar2 = 0;
      local_4 = 0xee893946;
    }
    local_8 = local_8 * 0x19660d + 0x3c6ef35f;
    local_4 = local_8 ^ local_4;
  } while( true );
}

