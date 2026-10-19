// FUN_10009c61c @ 10009c61c

void FUN_10009c61c(long *param_1,undefined8 param_2,undefined8 param_3,int *param_4,int param_5,
                  uint *param_6,long param_7)

{
  code *pcVar1;
  int iVar2;
  long lVar3;
  ulong uVar4;
  ulong uVar5;
  
  *param_1 = param_7;
  param_1[1] = 0;
  param_1[2] = 0;
  *(undefined4 *)(param_1 + 3) = 0;
  if (*param_4 != param_5) {
    return;
  }
  if (DAT_100106078 == (code *)0x0) {
    if (DAT_100106080 == (code *)0x0) {
      DAT_100106078 = (code *)FUN_10009b6b4(0xcfcd35ca777edf28);
      DAT_100106080 = DAT_100106078;
      if (DAT_100106078 == (code *)0x0) {
        return;
      }
    }
    else {
      DAT_100106078 = DAT_100106080;
    }
  }
  uVar4 = (ulong)*param_6;
  if (*param_6 == 0) {
    return;
  }
  if (DAT_100106088 == (code *)0x0) {
    if (DAT_100106090 == (code *)0x0) {
      DAT_100106088 = (code *)FUN_10009b6b4(0x34c313e25d2447d1);
      DAT_100106090 = DAT_100106088;
      if (DAT_100106088 == (code *)0x0) {
        return;
      }
    }
    else {
      DAT_100106088 = DAT_100106090;
    }
  }
  uVar5 = uVar4 + 0x3fff & 0x1ffffc000;
  lVar3 = (*DAT_100106078)(0,uVar5,3,0x1002,0xffffffff,0);
  if (1 < lVar3 + 1U) {
    FUN_10009c96c(lVar3,param_7,uVar4,param_2,param_3);
    iVar2 = (*DAT_100106088)(lVar3,uVar5,5);
    if (iVar2 == 0) goto LAB_10009c82c;
  }
  lVar3 = (*DAT_100106078)(0,uVar5,7,0x1802,0xffffffff,0);
  if (1 < lVar3 + 1U) {
    pcVar1 = DAT_100106098;
    if (((DAT_1001060a0 & 1) == 0) &&
       (DAT_1001060a0 = 1, pcVar1 = DAT_1001060a8, DAT_1001060a8 == (code *)0x0)) {
      DAT_1001060a8 = (code *)FUN_10009b6b4(0xce7336ae584ef060);
      pcVar1 = DAT_1001060a8;
    }
    DAT_100106098 = pcVar1;
    if (DAT_100106098 == (code *)0x0) {
      FUN_10009c96c(lVar3,param_7,uVar4,param_2,param_3);
    }
    else {
      (*DAT_100106098)(0);
      pcVar1 = DAT_100106098;
      FUN_10009c96c(lVar3,param_7,uVar4,param_2,param_3);
      if (pcVar1 != (code *)0x0) {
        (*pcVar1)(1);
      }
    }
  }
  if (lVar3 + 1U < 2) {
    return;
  }
LAB_10009c82c:
  pcVar1 = DAT_1001060b0;
  if (((DAT_1001060b8 & 1) == 0) &&
     (DAT_1001060b8 = 1, pcVar1 = DAT_1001060c0, DAT_1001060c0 == (code *)0x0)) {
    DAT_1001060c0 = (code *)FUN_10009b6b4(0xba190400a759187d);
    pcVar1 = DAT_1001060c0;
  }
  DAT_1001060b0 = pcVar1;
  if (DAT_1001060b0 == (code *)0x0) {
    ___clear_cache(lVar3,lVar3 + uVar5);
  }
  else {
    (*DAT_1001060b0)(lVar3,uVar5);
  }
  *param_1 = lVar3;
  param_1[1] = uVar4;
  param_1[2] = uVar5;
  *(undefined4 *)(param_1 + 3) = 1;
  return;
}

