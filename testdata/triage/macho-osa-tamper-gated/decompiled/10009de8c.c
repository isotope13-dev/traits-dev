// FUN_10009de8c @ 10009de8c

void FUN_10009de8c(long param_1,ulong param_2,byte param_3,long param_4)

{
  byte *pbVar1;
  byte *pbVar2;
  char cVar3;
  long lVar4;
  ulong uVar5;
  long lVar6;
  
  if (param_2 != 0) {
    lVar4 = 0;
    uVar5 = (param_2 - 1) % 6;
    lVar6 = 0;
    if (uVar5 != 5) {
      lVar6 = uVar5 + 1;
    }
    if (5 < param_2) {
      lVar4 = 0;
      do {
        pbVar1 = (byte *)(param_1 + 5 + lVar4);
        cVar3 = (char)lVar4;
        pbVar2 = (byte *)(param_4 + lVar4);
        *pbVar2 = cVar3 * 'U' ^ param_3 ^ pbVar1[-5];
        pbVar2[1] = cVar3 * 'U' + 0x55U ^ pbVar1[-4] ^ param_3;
        pbVar2[2] = (cVar3 + '\x02') * 'U' ^ pbVar1[-3] ^ param_3;
        pbVar2[3] = (cVar3 + '\x03') * 'U' ^ pbVar1[-2] ^ param_3;
        pbVar2[4] = (cVar3 + '\x04') * 'U' ^ pbVar1[-1] ^ param_3;
        pbVar2[5] = (cVar3 + '\x05') * 'U' ^ *pbVar1 ^ param_3;
        lVar4 = lVar4 + 6;
      } while (param_2 - lVar6 != lVar4);
    }
    if (uVar5 != 5) {
      do {
        *(byte *)(param_4 + lVar4) = (char)lVar4 * 'U' ^ param_3 ^ *(byte *)(param_1 + lVar4);
        lVar4 = lVar4 + 1;
        lVar6 = lVar6 + -1;
      } while (lVar6 != 0);
    }
  }
  *(undefined1 *)(param_4 + param_2) = 0;
  return;
}

