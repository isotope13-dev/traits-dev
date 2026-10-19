// FUN_10009bc14 @ 10009bc14

void FUN_10009bc14(int *param_1,long param_2,undefined8 param_3)

{
  int *piVar1;
  ulong uVar2;
  uint uVar3;
  int iVar4;
  undefined8 uVar5;
  int iVar6;
  uint uVar7;
  long lVar8;
  long lVar9;
  uint uVar10;
  int *piVar11;
  undefined1 auStack_1028 [4096];
  long local_28;
  
  local_28 = *(long *)PTR____stack_chk_guard_100102830;
  if (*param_1 == -0x1120531) {
    uVar5 = 0;
    iVar6 = param_1[4];
    if ((0xffffefff < iVar6 - 0x1001U) && (0xffefffff < param_1[5] - 0x100001U)) {
      lVar8 = 0;
      lVar9 = 0;
      uVar10 = 0;
      uVar7 = 0;
      piVar1 = (int *)((long)(param_1 + 8) + (ulong)(uint)param_1[5]);
      piVar11 = param_1 + 8;
      do {
        if (piVar1 < piVar11 + 2) {
          uVar5 = 0;
          goto LAB_10009bcf4;
        }
        uVar3 = piVar11[1];
        if (uVar3 < 8) {
          uVar5 = 0;
          goto LAB_10009bcf4;
        }
        if (piVar1 < (int *)((long)piVar11 + (ulong)uVar3)) {
          uVar5 = 0;
          goto LAB_10009bcf4;
        }
        iVar4 = *piVar11;
        if ((iVar4 == 0x19) && (0x2f < uVar3)) {
          if (((((((char)piVar11[2] == '_') && (*(char *)((long)piVar11 + 9) == '_')) &&
                (*(char *)((long)piVar11 + 10) == 'L')) &&
               (((*(char *)((long)piVar11 + 0xb) == 'I' && ((char)piVar11[3] == 'N')) &&
                ((*(char *)((long)piVar11 + 0xd) == 'K' &&
                 ((*(char *)((long)piVar11 + 0xe) == 'E' && (*(char *)((long)piVar11 + 0xf) == 'D'))
                 )))))) && ((char)piVar11[4] == 'I')) &&
             ((*(char *)((long)piVar11 + 0x11) == 'T' && (*(char *)((long)piVar11 + 0x12) == '\0')))
             ) {
            lVar8 = *(long *)(piVar11 + 6);
            lVar9 = *(long *)(piVar11 + 10);
          }
        }
        else if ((uVar3 < 0x10) || (iVar4 != -0x7fffffcd)) {
          if (iVar4 == 0x22) {
            if (0x2f < uVar3) {
LAB_10009beac:
              uVar10 = piVar11[10];
              uVar7 = piVar11[0xb];
            }
          }
          else if ((0x2f < uVar3) && (iVar4 == -0x7fffffde)) goto LAB_10009beac;
        }
        else {
          uVar10 = piVar11[2];
          uVar7 = piVar11[3];
        }
        iVar6 = iVar6 + -1;
        piVar11 = (int *)((long)piVar11 + (ulong)uVar3);
      } while (iVar6 != 0);
      uVar5 = 0;
      if ((((uVar10 != 0) && (uVar7 != 0)) && (lVar8 != 0)) && (uVar7 < 0x1000001)) {
        piVar1 = (int *)(((param_2 + (ulong)uVar10) - lVar9) + lVar8);
        uVar2 = (long)piVar1 - (long)param_1;
        if (piVar1 < param_1 || (long)piVar1 - (long)param_1 == 0) {
          uVar2 = (long)param_1 - (long)piVar1;
        }
        if (uVar2 < 0x800000001) {
          uVar5 = FUN_10009bf30(piVar1,uVar7,0,param_1,param_3,auStack_1028,0);
        }
        else {
          uVar5 = 0;
        }
      }
    }
  }
  else {
    uVar5 = 0;
  }
LAB_10009bcf4:
  if (*(long *)PTR____stack_chk_guard_100102830 != local_28) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail(uVar5);
  }
  return;
}

