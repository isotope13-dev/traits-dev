// FUN_10009c33c @ 10009c33c

ulong FUN_10009c33c(char *param_1)

{
  byte *pbVar1;
  size_t sVar2;
  ulong uVar3;
  ulong uVar4;
  ulong uVar5;
  ulong uVar6;
  ulong uVar7;
  ulong uVar8;
  ulong uVar9;
  ulong uVar10;
  
  uVar9 = DAT_10009ecc0;
  uVar7 = DAT_10009ecb8;
  uVar5 = DAT_10009ecb0;
  uVar10 = DAT_10009eca8;
  uVar6 = DAT_10009eca0;
  uVar3 = DAT_10009ec98;
  uVar8 = DAT_10009ec90;
  uVar4 = DAT_10009ec88;
  sVar2 = _strlen(param_1);
  uVar8 = uVar8 ^ uVar4;
  uVar6 = uVar6 ^ uVar3;
  uVar5 = uVar5 ^ uVar10;
  uVar9 = uVar9 ^ uVar7;
  uVar3 = sVar2 & 7;
  uVar4 = sVar2 & 0xfffffffffffffff8;
  if (uVar4 != 0) {
    uVar10 = 0;
    do {
      uVar9 = *(ulong *)(param_1 + uVar10) ^ uVar9;
      uVar8 = uVar8 + uVar6;
      uVar7 = uVar8 ^ (uVar6 >> 0x33 | uVar6 << 0xd);
      uVar6 = uVar9 + uVar5 + uVar7;
      uVar5 = uVar9 + uVar5 ^ (uVar9 >> 0x30 | uVar9 << 0x10);
      uVar7 = uVar6 ^ (uVar7 >> 0x2f | uVar7 << 0x11);
      uVar9 = uVar5 + (uVar8 >> 0x20 | uVar8 << 0x20);
      uVar8 = uVar9 + uVar7;
      uVar9 = uVar9 ^ (uVar5 >> 0x2b | uVar5 << 0x15);
      uVar7 = uVar8 ^ (uVar7 >> 0x33 | uVar7 << 0xd);
      uVar6 = uVar9 + (uVar6 >> 0x20 | uVar6 << 0x20);
      uVar5 = uVar6 + uVar7;
      uVar6 = uVar6 ^ (uVar9 >> 0x30 | uVar9 << 0x10);
      uVar9 = uVar6 + (uVar8 >> 0x20 | uVar8 << 0x20);
      uVar8 = uVar9 ^ *(ulong *)(param_1 + uVar10);
      uVar9 = uVar9 ^ (uVar6 >> 0x2b | uVar6 << 0x15);
      uVar6 = uVar5 ^ (uVar7 >> 0x2f | uVar7 << 0x11);
      uVar5 = uVar5 >> 0x20 | uVar5 << 0x20;
      uVar10 = uVar10 + 8;
    } while (uVar10 < uVar4);
  }
  uVar10 = sVar2 << 0x38;
  if (uVar3 != 0) {
    pbVar1 = (byte *)(param_1 + uVar4);
    uVar10 = uVar10 | *pbVar1;
    if ((((uVar3 != 1) && (uVar10 = uVar10 | (ulong)pbVar1[1] << 8, uVar3 != 2)) &&
        (uVar10 = uVar10 | (ulong)pbVar1[2] << 0x10, uVar3 != 3)) &&
       (((uVar10 = uVar10 | (ulong)pbVar1[3] << 0x18, uVar3 != 4 &&
         (uVar10 = uVar10 | (ulong)pbVar1[4] << 0x20, uVar3 != 5)) &&
        (uVar10 = uVar10 | (ulong)pbVar1[5] << 0x28, uVar3 != 6)))) {
      uVar10 = uVar10 | (ulong)pbVar1[6] << 0x30;
    }
  }
  uVar9 = uVar10 ^ uVar9;
  uVar8 = uVar8 + uVar6;
  uVar6 = uVar8 ^ (uVar6 >> 0x33 | uVar6 << 0xd);
  uVar4 = uVar9 + uVar5 + uVar6;
  uVar3 = uVar9 + uVar5 ^ (uVar9 >> 0x30 | uVar9 << 0x10);
  uVar6 = uVar4 ^ (uVar6 >> 0x2f | uVar6 << 0x11);
  uVar9 = uVar3 + (uVar8 >> 0x20 | uVar8 << 0x20);
  uVar8 = uVar9 + uVar6;
  uVar9 = uVar9 ^ (uVar3 >> 0x2b | uVar3 << 0x15);
  uVar5 = uVar8 ^ (uVar6 >> 0x33 | uVar6 << 0xd);
  uVar4 = uVar9 + (uVar4 >> 0x20 | uVar4 << 0x20);
  uVar3 = uVar4 + uVar5;
  uVar4 = uVar4 ^ (uVar9 >> 0x30 | uVar9 << 0x10);
  uVar9 = uVar4 + (uVar8 >> 0x20 | uVar8 << 0x20);
  uVar6 = uVar9 ^ (uVar4 >> 0x2b | uVar4 << 0x15);
  uVar8 = uVar3 ^ (uVar5 >> 0x2f | uVar5 << 0x11);
  uVar9 = (uVar9 ^ uVar10) + uVar8;
  uVar10 = uVar9 ^ (uVar8 >> 0x33 | uVar8 << 0xd);
  uVar8 = ((uVar3 >> 0x20 | uVar3 << 0x20) ^ 0xff) + uVar6;
  uVar4 = uVar10 + uVar8;
  uVar8 = uVar8 ^ (uVar6 >> 0x30 | uVar6 << 0x10);
  uVar6 = uVar4 ^ (uVar10 >> 0x2f | uVar10 << 0x11);
  uVar9 = (uVar9 >> 0x20 | uVar9 << 0x20) + uVar8;
  uVar3 = uVar6 + uVar9;
  uVar9 = uVar9 ^ (uVar8 >> 0x2b | uVar8 << 0x15);
  uVar6 = uVar3 ^ (uVar6 >> 0x33 | uVar6 << 0xd);
  uVar8 = (uVar4 >> 0x20 | uVar4 << 0x20) + uVar9;
  uVar4 = uVar6 + uVar8;
  uVar8 = uVar8 ^ (uVar9 >> 0x30 | uVar9 << 0x10);
  uVar6 = uVar4 ^ (uVar6 >> 0x2f | uVar6 << 0x11);
  uVar9 = (uVar3 >> 0x20 | uVar3 << 0x20) + uVar8;
  uVar3 = uVar6 + uVar9;
  uVar9 = uVar9 ^ (uVar8 >> 0x2b | uVar8 << 0x15);
  uVar6 = uVar3 ^ (uVar6 >> 0x33 | uVar6 << 0xd);
  uVar8 = (uVar4 >> 0x20 | uVar4 << 0x20) + uVar9;
  uVar4 = uVar6 + uVar8;
  uVar8 = uVar8 ^ (uVar9 >> 0x30 | uVar9 << 0x10);
  uVar6 = uVar4 ^ (uVar6 >> 0x2f | uVar6 << 0x11);
  uVar9 = (uVar3 >> 0x20 | uVar3 << 0x20) + uVar8;
  uVar3 = uVar9 ^ (uVar8 >> 0x2b | uVar8 << 0x15);
  uVar6 = uVar6 + uVar9 ^ (uVar6 >> 0x33 | uVar6 << 0xd);
  uVar9 = (uVar4 >> 0x20 | uVar4 << 0x20) + uVar3;
  uVar8 = uVar6 + uVar9;
  uVar9 = uVar9 ^ (uVar3 >> 0x30 | uVar3 << 0x10);
  return (uVar9 >> 0x2b | uVar9 << 0x15) ^ (uVar6 >> 0x2f | uVar6 << 0x11) ^
         (uVar8 >> 0x20 | uVar8 << 0x20) ^ uVar8;
}

