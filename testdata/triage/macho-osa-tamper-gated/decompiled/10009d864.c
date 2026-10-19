// FUN_10009d864 @ 10009d864

void FUN_10009d864(void *param_1,size_t param_2,byte *param_3,long param_4,uint *param_5)

{
  byte *pbVar1;
  ulong uVar2;
  uint uVar3;
  uint uVar4;
  long lVar5;
  long lVar6;
  ulong uVar7;
  long lVar8;
  undefined8 local_1b8;
  undefined8 local_1b0;
  undefined8 local_1a8;
  undefined8 local_1a0;
  long local_198;
  byte local_190 [64];
  ulong local_150;
  uint local_148;
  uint uStack_144;
  uint local_140;
  uint local_13c;
  uint uStack_138;
  uint local_134;
  uint uStack_130;
  uint local_12c;
  byte local_128 [64];
  byte local_e8 [64];
  byte abStack_a8 [64];
  long local_68;
  
  local_68 = *(long *)PTR____stack_chk_guard_100102830;
  _memcpy(abStack_a8,param_1,param_2);
  _bzero(abStack_a8 + param_2,0x40 - param_2);
  lVar6 = 0x3f;
  do {
    local_e8[lVar6] = abStack_a8[lVar6] ^ 0x36;
    local_128[lVar6] = abStack_a8[lVar6] ^ 0x5c;
    lVar6 = lVar6 + -1;
  } while (lVar6 != -1);
  FUN_10009d668();
  lVar8 = 0;
  local_150 = 0;
  lVar6 = 0;
  local_1b8 = DAT_1001060c8;
  local_1b0 = DAT_1001060d0;
  local_1a8 = DAT_1001060d8;
  local_1a0 = DAT_1001060e0;
  local_198 = 0;
  do {
    pbVar1 = local_190 + local_150;
    local_150 = local_150 + 1;
    *pbVar1 = local_e8[lVar6];
    if (local_150 == 0x40) {
      FUN_10009d22c(&local_1b8);
      local_150 = 0;
      lVar8 = local_198 + 0x200;
      local_198 = lVar8;
    }
    lVar6 = lVar6 + 1;
    lVar5 = local_150;
  } while (lVar6 != 0x40);
  for (; param_4 != 0; param_4 = param_4 + -1) {
    local_150 = lVar5 + 1;
    local_190[lVar5] = *param_3;
    if (local_150 == 0x40) {
      FUN_10009d22c(&local_1b8);
      local_150 = 0;
      lVar8 = local_198 + 0x200;
      local_198 = lVar8;
    }
    lVar5 = local_150;
    param_3 = param_3 + 1;
  }
  local_198 = lVar8 + lVar5 * 8;
  uVar3 = local_148 >> 8;
  local_148 = CONCAT31((int3)uVar3,0x80);
  local_150 = lVar5 + 1;
  local_190[lVar5] = 0x80;
  uVar7 = local_150;
  uVar2 = local_150;
  if (local_150 < 0x39) goto joined_r0x00010009dab4;
  if (local_150 < 0x40) {
    uVar2 = local_150 + 1;
    pbVar1 = local_190 + local_150;
    local_150 = uVar2;
    *pbVar1 = 0;
    if (uVar2 != 0x40) {
      local_150 = uVar7 + 2;
      local_190[uVar7 + 1] = 0;
      if (uVar7 + 2 != 0x40) {
        local_150 = uVar7 + 3;
        local_190[uVar7 + 2] = 0;
        if (uVar7 + 3 != 0x40) {
          local_150 = uVar7 + 4;
          local_190[uVar7 + 3] = 0;
          if (uVar7 + 4 != 0x40) {
            local_150 = uVar7 + 5;
            local_190[uVar7 + 4] = 0;
            if (uVar7 + 5 != 0x40) {
              local_150 = uVar7 + 6;
              local_190[uVar7 + 5] = 0;
              if (uVar7 + 6 != 0x40) {
                local_150 = uVar7 + 7;
                local_190[uVar7 + 6] = 0;
              }
            }
          }
        }
      }
    }
  }
  FUN_10009d22c(&local_1b8);
  uVar7 = 0;
  do {
    local_150 = uVar7 + 1;
    local_190[uVar7] = 0;
    uVar7 = uVar7 + 1;
    uVar2 = local_150;
joined_r0x00010009dab4:
  } while (uVar7 != 0x38);
  local_150 = uVar2 + 1;
  local_190[uVar2] = (byte)((ulong)local_198 >> 0x38);
  pbVar1 = local_190 + local_150;
  local_150 = local_150 + 1;
  *pbVar1 = (byte)((ulong)local_198 >> 0x30);
  pbVar1 = local_190 + local_150;
  local_150 = local_150 + 1;
  *pbVar1 = (byte)((ulong)local_198 >> 0x28);
  pbVar1 = local_190 + local_150;
  local_150 = local_150 + 1;
  *pbVar1 = (byte)((ulong)local_198 >> 0x20);
  pbVar1 = local_190 + local_150;
  local_150 = local_150 + 1;
  *pbVar1 = (byte)((ulong)local_198 >> 0x18);
  pbVar1 = local_190 + local_150;
  local_150 = local_150 + 1;
  *pbVar1 = (byte)((ulong)local_198 >> 0x10);
  pbVar1 = local_190 + local_150;
  local_150 = local_150 + 1;
  *pbVar1 = (byte)((ulong)local_198 >> 8);
  pbVar1 = local_190 + local_150;
  local_150 = local_150 + 1;
  *pbVar1 = (byte)local_198;
  FUN_10009d22c(&local_1b8);
  lVar8 = 0;
  local_150 = 0;
  lVar6 = 0;
  uVar3 = ((uint)local_1b8 & 0xff00ff00) >> 8 | ((uint)local_1b8 & 0xff00ff) << 8;
  uVar4 = (local_1b8._4_4_ & 0xff00ff00) >> 8 | (local_1b8._4_4_ & 0xff00ff) << 8;
  local_148 = uVar3 >> 0x10 | uVar3 << 0x10;
  uStack_144 = uVar4 >> 0x10 | uVar4 << 0x10;
  uVar3 = ((uint)local_1b0 & 0xff00ff00) >> 8 | ((uint)local_1b0 & 0xff00ff) << 8;
  local_140 = uVar3 >> 0x10 | uVar3 << 0x10;
  uVar3 = (local_1b0._4_4_ & 0xff00ff00) >> 8 | (local_1b0._4_4_ & 0xff00ff) << 8;
  uVar4 = ((uint)local_1a8 & 0xff00ff00) >> 8 | ((uint)local_1a8 & 0xff00ff) << 8;
  local_13c = uVar3 >> 0x10 | uVar3 << 0x10;
  uStack_138 = uVar4 >> 0x10 | uVar4 << 0x10;
  uVar3 = (local_1a8._4_4_ & 0xff00ff00) >> 8 | (local_1a8._4_4_ & 0xff00ff) << 8;
  uVar4 = ((uint)local_1a0 & 0xff00ff00) >> 8 | ((uint)local_1a0 & 0xff00ff) << 8;
  local_134 = uVar3 >> 0x10 | uVar3 << 0x10;
  uStack_130 = uVar4 >> 0x10 | uVar4 << 0x10;
  uVar3 = (local_1a0._4_4_ & 0xff00ff00) >> 8 | (local_1a0._4_4_ & 0xff00ff) << 8;
  local_12c = uVar3 >> 0x10 | uVar3 << 0x10;
  local_1a8 = DAT_1001060d8;
  local_1a0 = DAT_1001060e0;
  local_1b8 = DAT_1001060c8;
  local_1b0 = DAT_1001060d0;
  local_198 = 0;
  do {
    pbVar1 = local_190 + local_150;
    local_150 = local_150 + 1;
    *pbVar1 = local_128[lVar6];
    if (local_150 == 0x40) {
      FUN_10009d22c(&local_1b8);
      local_150 = 0;
      lVar8 = local_198 + 0x200;
      local_198 = lVar8;
    }
    lVar6 = lVar6 + 1;
  } while (lVar6 != 0x40);
  lVar6 = 0;
  do {
    pbVar1 = local_190 + local_150;
    local_150 = local_150 + 1;
    *pbVar1 = *(byte *)((long)&local_148 + lVar6);
    if (local_150 == 0x40) {
      FUN_10009d22c(&local_1b8);
      local_150 = 0;
      lVar8 = local_198 + 0x200;
      local_198 = lVar8;
    }
    lVar6 = lVar6 + 1;
  } while (lVar6 != 0x20);
  local_198 = lVar8 + local_150 * 8;
  pbVar1 = local_190 + local_150;
  local_150 = local_150 + 1;
  *pbVar1 = 0x80;
  uVar7 = local_150;
  if (local_150 < 0x39) {
    if (local_150 == 0x38) goto LAB_10009dd6c;
  }
  else {
    if (local_150 < 0x40) {
      uVar2 = local_150 + 1;
      pbVar1 = local_190 + local_150;
      local_150 = uVar2;
      *pbVar1 = 0;
      if (uVar2 != 0x40) {
        local_150 = uVar7 + 2;
        local_190[uVar7 + 1] = 0;
        if (uVar7 + 2 != 0x40) {
          local_150 = uVar7 + 3;
          local_190[uVar7 + 2] = 0;
          if (uVar7 + 3 != 0x40) {
            local_150 = uVar7 + 4;
            local_190[uVar7 + 3] = 0;
            if (uVar7 + 4 != 0x40) {
              local_150 = uVar7 + 5;
              local_190[uVar7 + 4] = 0;
              if (uVar7 + 5 != 0x40) {
                local_150 = uVar7 + 6;
                local_190[uVar7 + 5] = 0;
                if (uVar7 + 6 != 0x40) {
                  local_150 = uVar7 + 7;
                  local_190[uVar7 + 6] = 0;
                }
              }
            }
          }
        }
      }
    }
    FUN_10009d22c(&local_1b8);
    uVar7 = 0;
  }
  do {
    uVar2 = uVar7 + 1;
    local_150 = uVar2;
    local_190[uVar7] = 0;
    uVar7 = uVar2;
  } while (uVar2 != 0x38);
LAB_10009dd6c:
  pbVar1 = local_190 + local_150;
  local_150 = local_150 + 1;
  *pbVar1 = (byte)((ulong)local_198 >> 0x38);
  pbVar1 = local_190 + local_150;
  local_150 = local_150 + 1;
  *pbVar1 = (byte)((ulong)local_198 >> 0x30);
  pbVar1 = local_190 + local_150;
  local_150 = local_150 + 1;
  *pbVar1 = (byte)((ulong)local_198 >> 0x28);
  pbVar1 = local_190 + local_150;
  local_150 = local_150 + 1;
  *pbVar1 = (byte)((ulong)local_198 >> 0x20);
  pbVar1 = local_190 + local_150;
  local_150 = local_150 + 1;
  *pbVar1 = (byte)((ulong)local_198 >> 0x18);
  pbVar1 = local_190 + local_150;
  local_150 = local_150 + 1;
  *pbVar1 = (byte)((ulong)local_198 >> 0x10);
  pbVar1 = local_190 + local_150;
  local_150 = local_150 + 1;
  *pbVar1 = (byte)((ulong)local_198 >> 8);
  pbVar1 = local_190 + local_150;
  local_150 = local_150 + 1;
  *pbVar1 = (byte)local_198;
  FUN_10009d22c(&local_1b8);
  uVar3 = ((uint)local_1b8 & 0xff00ff00) >> 8 | ((uint)local_1b8 & 0xff00ff) << 8;
  uVar4 = (local_1b8._4_4_ & 0xff00ff00) >> 8 | (local_1b8._4_4_ & 0xff00ff) << 8;
  *param_5 = uVar3 >> 0x10 | uVar3 << 0x10;
  param_5[1] = uVar4 >> 0x10 | uVar4 << 0x10;
  uVar3 = ((uint)local_1b0 & 0xff00ff00) >> 8 | ((uint)local_1b0 & 0xff00ff) << 8;
  uVar4 = (local_1b0._4_4_ & 0xff00ff00) >> 8 | (local_1b0._4_4_ & 0xff00ff) << 8;
  param_5[2] = uVar3 >> 0x10 | uVar3 << 0x10;
  param_5[3] = uVar4 >> 0x10 | uVar4 << 0x10;
  uVar3 = ((uint)local_1a8 & 0xff00ff00) >> 8 | ((uint)local_1a8 & 0xff00ff) << 8;
  uVar4 = (local_1a8._4_4_ & 0xff00ff00) >> 8 | (local_1a8._4_4_ & 0xff00ff) << 8;
  param_5[4] = uVar3 >> 0x10 | uVar3 << 0x10;
  param_5[5] = uVar4 >> 0x10 | uVar4 << 0x10;
  uVar3 = ((uint)local_1a0 & 0xff00ff00) >> 8 | ((uint)local_1a0 & 0xff00ff) << 8;
  uVar4 = (local_1a0._4_4_ & 0xff00ff00) >> 8 | (local_1a0._4_4_ & 0xff00ff) << 8;
  param_5[6] = uVar3 >> 0x10 | uVar3 << 0x10;
  param_5[7] = uVar4 >> 0x10 | uVar4 << 0x10;
  if (*(long *)PTR____stack_chk_guard_100102830 == local_68) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

