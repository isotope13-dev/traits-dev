// FUN_10009ba50 @ 10009ba50

bool FUN_10009ba50(int *param_1,long *param_2)

{
  int *piVar1;
  uint uVar2;
  int iVar3;
  int *piVar4;
  
  if (*param_1 != -0x1120531) {
    return DAT_100105f9d != '\0';
  }
  iVar3 = param_1[4];
  if (iVar3 - 0x1001U < 0xfffff000) {
    return DAT_100105f9d != '\0';
  }
  if (param_1[5] - 0x100001U < 0xfff00000) {
    return false;
  }
  piVar1 = (int *)((long)(param_1 + 8) + (ulong)(uint)param_1[5]);
  piVar4 = param_1 + 8;
  while( true ) {
    if (piVar1 < piVar4 + 2) {
      return false;
    }
    uVar2 = piVar4[1];
    if (uVar2 < 8) {
      return false;
    }
    if (piVar1 < (int *)((long)piVar4 + (ulong)uVar2)) {
      return false;
    }
    if ((((((*piVar4 == 0x19) && (0x1f < uVar2)) && ((char)piVar4[2] == '_')) &&
         ((*(char *)((long)piVar4 + 9) == '_' && (*(char *)((long)piVar4 + 10) == 'T')))) &&
        ((*(char *)((long)piVar4 + 0xb) == 'E' &&
         (((char)piVar4[3] == 'X' && (*(char *)((long)piVar4 + 0xd) == 'T')))))) &&
       (*(char *)((long)piVar4 + 0xe) == '\0')) break;
    iVar3 = iVar3 + -1;
    piVar4 = (int *)((long)piVar4 + (ulong)uVar2);
    if (iVar3 == 0) {
      return false;
    }
  }
  *param_2 = (long)param_1 - *(long *)(piVar4 + 6);
  return true;
}

