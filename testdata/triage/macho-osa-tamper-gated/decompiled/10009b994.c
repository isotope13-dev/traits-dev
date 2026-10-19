// FUN_10009b994 @ 10009b994

void FUN_10009b994(byte *param_1,long param_2,long param_3,byte *param_4)

{
  ulong uVar1;
  byte *pbVar2;
  long lVar3;
  
  if (param_2 != 0) {
    uVar1 = 0;
    pbVar2 = param_4;
    lVar3 = param_2;
    do {
      *pbVar2 = *(byte *)(param_3 + (uVar1 / 0xd) * -0xd) ^ *param_1;
      uVar1 = uVar1 + 1;
      param_3 = param_3 + 1;
      lVar3 = lVar3 + -1;
      param_1 = param_1 + 1;
      pbVar2 = pbVar2 + 1;
    } while (lVar3 != 0);
  }
  param_4[param_2] = 0;
  return;
}

