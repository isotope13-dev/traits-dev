// FUN_10008f254 @ 10008f254

void FUN_10008f254(void)

{
  byte bVar1;
  byte bVar2;
  bool bVar3;
  int iVar4;
  long lVar5;
  uint uVar6;
  byte *pbVar7;
  long lVar8;
  long lVar9;
  undefined8 local_70;
  undefined8 uStack_68;
  byte local_60 [40];
  undefined8 local_38;
  undefined8 local_30;
  long local_28;
  
  local_28 = *(long *)PTR____stack_chk_guard_100102830;
  if (DAT_1001062e8 == (code *)0x0) {
    DAT_1001062e8 = (code *)FUN_10009b6b4(0xe3bd3617e6f5e4ea);
    bVar3 = false;
    if (DAT_1001062e8 == (code *)0x0) goto LAB_10008f484;
  }
  local_38 = 0;
  local_30 = 0;
  local_70 = 1;
  uStack_68 = 0;
  iVar4 = (*DAT_1001062e8)(&local_38,&local_70);
  if (iVar4 == 0) {
    lVar5 = 0;
    lVar8 = 0;
    do {
      iVar4 = (int)lVar8;
      uVar6 = (uint)lVar5 & 0xd;
      if (uVar6 == 8 || uVar6 == 4) {
        local_60[iVar4] = 0x2d;
        iVar4 = iVar4 + 1;
      }
      bVar2 = *(byte *)((long)&local_38 + lVar5);
      bVar1 = bVar2 >> 4 | 0x30;
      if (0x9f < bVar2) {
        bVar1 = (bVar2 >> 4) + 0x57;
      }
      lVar9 = (long)iVar4;
      local_60[lVar9] = bVar1;
      bVar1 = bVar2 & 0xf | 0x30;
      if (9 < (bVar2 & 0xf)) {
        bVar1 = (bVar2 & 0xf) + 0x57;
      }
      lVar8 = lVar9 + 2;
      local_60[lVar9 + 1] = bVar1;
      lVar5 = lVar5 + 1;
    } while (lVar5 != 0x10);
    pbVar7 = local_60;
    pbVar7[lVar8] = 0;
    iVar4 = 0x1505;
    uVar6 = (uint)local_60[0];
    if (local_60[0] != 0) {
      do {
        pbVar7 = pbVar7 + 1;
        iVar4 = iVar4 * 0x21 + uVar6;
        uVar6 = (uint)*pbVar7;
      } while (uVar6 != 0);
    }
    local_60[0] = 0;
    local_60[1] = 0;
    local_60[2] = 0;
    local_60[3] = 0;
    local_60[4] = 0;
    local_60[5] = 0;
    local_60[6] = 0;
    local_60[7] = 0;
    local_60[8] = 0;
    local_60[9] = 0;
    local_60[10] = 0;
    local_60[0xb] = 0;
    local_60[0xc] = 0;
    local_60[0xd] = 0;
    local_60[0xe] = 0;
    local_60[0xf] = 0;
    local_60[0x10] = 0;
    local_60[0x11] = 0;
    local_60[0x12] = 0;
    local_60[0x13] = 0;
    local_60[0x14] = 0;
    local_60[0x15] = 0;
    local_60[0x16] = 0;
    local_60[0x17] = 0;
    local_60[0x18] = 0;
    local_60[0x19] = 0;
    local_60[0x1a] = 0;
    local_60[0x1b] = 0;
    local_60[0x1c] = 0;
    local_60[0x1d] = 0;
    local_60[0x1e] = 0;
    local_60[0x1f] = 0;
    local_60[0x20] = 0;
    local_60[0x21] = 0;
    local_60[0x22] = 0;
    local_60[0x23] = 0;
    local_60[0x24] = 0;
    local_60[0x25] = 0;
    local_60[0x26] = 0;
    local_60[0x27] = 0;
    local_30 = 0;
    bVar3 = iVar4 == 0x676d1aa2;
    local_38 = 0;
  }
  else {
    bVar3 = false;
  }
LAB_10008f484:
  if (*(long *)PTR____stack_chk_guard_100102830 == local_28) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail(bVar3);
}

