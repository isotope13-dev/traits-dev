// FUN_100093a80 @ 100093a80

void FUN_100093a80(long param_1,long param_2,ulong param_3)

{
  ulong uVar1;
  byte bVar2;
  byte bVar3;
  byte bVar4;
  uint uVar5;
  int iVar6;
  int iVar7;
  byte *pbVar8;
  byte *pbVar9;
  byte *pbVar10;
  byte *pbVar11;
  long lVar12;
  ulong uVar13;
  
  if (param_3 != 0) {
    lVar12 = 0;
    uVar13 = 0;
    do {
      pbVar9 = (byte *)(param_1 + 3 + lVar12);
      pbVar11 = (byte *)(param_1 + 2 + lVar12);
      do {
        pbVar8 = pbVar9;
        uVar5 = (uint)*(byte *)(param_1 + lVar12) * 9 + 0xb5 ^
                (uint)(byte)(&DAT_10009f058)[*(byte *)(param_1 + lVar12)];
        lVar12 = lVar12 + 1;
        pbVar9 = pbVar8 + 1;
        pbVar10 = pbVar11;
        pbVar11 = pbVar11 + 1;
      } while ((uVar5 & 0xff) == 0xca);
      do {
        pbVar11 = pbVar8;
        bVar2 = *(byte *)(param_1 + lVar12) * '\t' + 0xb5 ^
                (&DAT_10009f058)[*(byte *)(param_1 + lVar12)];
        lVar12 = lVar12 + 1;
        pbVar9 = pbVar10;
        pbVar10 = pbVar10 + 1;
        pbVar8 = pbVar11 + 1;
      } while (bVar2 == 0xca);
      do {
        bVar3 = *pbVar9 * '\t' + 0xb5 ^ (&DAT_10009f058)[*pbVar9];
        lVar12 = lVar12 + 1;
        pbVar9 = pbVar9 + 1;
        pbVar10 = pbVar11;
        pbVar11 = pbVar11 + 1;
      } while (bVar3 == 0xca);
      do {
        bVar4 = *pbVar10 * '\t' + 0xb5 ^ (&DAT_10009f058)[*pbVar10];
        lVar12 = lVar12 + 1;
        pbVar10 = pbVar10 + 1;
      } while (bVar4 == 0xca);
      iVar6 = (uint)bVar2 << 0xc;
      iVar7 = (uint)bVar3 << 6;
      uVar1 = uVar13 + 1;
      *(byte *)(param_2 + uVar13) = (byte)((uint)iVar6 >> 0x10) | (byte)((uVar5 << 0x12) >> 0x10);
      if (uVar1 < param_3) {
        *(byte *)(param_2 + uVar1) = (byte)((uint)iVar7 >> 8) | (byte)((uint)iVar6 >> 8);
        uVar1 = uVar13 + 2;
      }
      uVar13 = uVar1;
      if (uVar13 < param_3) {
        *(byte *)(param_2 + uVar13) = bVar4 | (byte)iVar7;
        uVar13 = uVar13 + 1;
      }
    } while (uVar13 < param_3);
  }
  return;
}

