// FUN_10009bf30 @ 10009bf30

long FUN_10009bf30(long param_1,ulong param_2,ulong param_3,long param_4,long param_5,long param_6,
                  int param_7)

{
  byte *pbVar1;
  byte *pbVar2;
  byte bVar3;
  ulong uVar4;
  long lVar5;
  undefined8 uVar6;
  long lVar7;
  byte *pbVar8;
  uint uVar9;
  ulong uVar10;
  byte *local_70;
  byte *local_68;
  
  if (param_2 <= param_3) {
    return 0;
  }
  pbVar2 = (byte *)(param_1 + param_2);
  local_68 = (byte *)(param_1 + param_3);
  uVar4 = FUN_10009c1c0(&local_68,pbVar2);
  local_70 = local_68;
  if (local_68 <= pbVar2 && uVar4 <= (ulong)((long)pbVar2 - (long)local_68)) {
    if (uVar4 != 0) {
      *(undefined1 *)(param_6 + param_7) = 0;
      lVar5 = FUN_10009c33c(param_6);
      if (lVar5 == param_5) {
        uVar4 = FUN_10009c1c0(&local_70,pbVar2);
        if (((local_70 <= pbVar2) && ((uVar4 & 0x1b) == 0)) &&
           (lVar5 = FUN_10009c1c0(&local_70,pbVar2), local_70 <= pbVar2)) {
          return lVar5 + param_4;
        }
        return 0;
      }
    }
    local_70 = local_70 + uVar4;
    if ((local_70 < pbVar2) && (bVar3 = *local_70, bVar3 != 0)) {
      uVar9 = 0;
      pbVar8 = local_70 + 1;
      while( true ) {
        if (pbVar2 <= pbVar8) {
          return 0;
        }
        uVar10 = (param_2 + param_1) - (long)pbVar8;
        local_68 = pbVar8;
        for (uVar4 = uVar10 & 3; uVar4 != 0; uVar4 = uVar4 - 1) {
          if (*local_68 == 0) {
            local_68 = local_68 + 1;
            goto LAB_10009c0e4;
          }
          local_68 = local_68 + 1;
        }
        if (uVar10 - 1 < 3) break;
        local_68 = local_68 + 2;
        while (local_68[-2] != 0) {
          if (local_68[-1] == 0) goto LAB_10009c0e4;
          if (*local_68 == 0) {
            local_68 = local_68 + 1;
            goto LAB_10009c0e4;
          }
          if (local_68[1] == 0) {
            local_68 = local_68 + 2;
            goto LAB_10009c0e4;
          }
          pbVar1 = local_68 + 2;
          local_68 = local_68 + 4;
          if (pbVar1 == (byte *)(param_1 + param_2)) {
            return 0;
          }
        }
        local_68 = local_68 + -1;
LAB_10009c0e4:
        uVar6 = FUN_10009c1c0(&local_68,pbVar2);
        pbVar1 = local_68;
        lVar5 = (long)param_7;
        if (pbVar2 < local_68) {
          return 0;
        }
        do {
          lVar7 = lVar5;
          if ((*pbVar8 == 0) || (0xffe < lVar5)) break;
          lVar7 = lVar5 + 1;
          *(byte *)(param_6 + lVar5) = *pbVar8;
          uVar10 = uVar10 - 1;
          lVar5 = lVar7;
          pbVar8 = pbVar8 + 1;
        } while (uVar10 != 0);
        lVar5 = FUN_10009bf30(param_1,param_2,uVar6,param_4,param_5,param_6,lVar7);
        if (lVar5 != 0) {
          return lVar5;
        }
        uVar9 = uVar9 + 1;
        pbVar8 = pbVar1;
        if (bVar3 <= uVar9) {
          return 0;
        }
      }
    }
  }
  return 0;
}

