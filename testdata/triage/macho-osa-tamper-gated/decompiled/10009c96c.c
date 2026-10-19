// FUN_10009c96c @ 10009c96c

void FUN_10009c96c(long param_1,long param_2,ulong param_3,byte *param_4,byte *param_5)

{
  byte bVar1;
  byte bVar2;
  byte bVar3;
  byte bVar4;
  byte bVar5;
  byte bVar6;
  byte bVar7;
  byte bVar8;
  byte bVar9;
  byte bVar10;
  byte bVar11;
  byte bVar12;
  byte bVar13;
  byte bVar14;
  byte bVar15;
  byte bVar16;
  byte bVar17;
  byte bVar18;
  byte bVar19;
  byte bVar20;
  byte bVar21;
  byte bVar22;
  byte bVar23;
  byte bVar24;
  byte bVar25;
  byte bVar26;
  byte bVar27;
  byte bVar28;
  byte bVar29;
  byte bVar30;
  byte bVar31;
  byte bVar32;
  byte bVar33;
  byte bVar34;
  byte bVar35;
  byte bVar36;
  byte bVar37;
  byte bVar38;
  byte bVar39;
  byte bVar40;
  byte bVar41;
  byte bVar42;
  byte bVar43;
  byte bVar44;
  byte bVar45;
  byte bVar46;
  byte bVar47;
  byte bVar48;
  bool bVar49;
  ulong uVar50;
  ulong uVar51;
  ulong uVar52;
  ulong uVar53;
  ulong uVar54;
  ulong uVar55;
  ulong uVar56;
  
  uVar50 = 0;
  bVar1 = param_4[8];
  bVar2 = param_5[8];
  bVar3 = param_4[9];
  bVar4 = param_5[9];
  bVar5 = param_4[10];
  bVar6 = param_5[10];
  bVar7 = param_4[0xb];
  bVar8 = param_5[0xb];
  bVar9 = param_4[0xc];
  bVar10 = param_5[0xc];
  bVar11 = param_4[0xd];
  bVar12 = param_5[0xd];
  bVar13 = param_4[0xe];
  bVar14 = param_5[0xe];
  bVar15 = param_4[0xf];
  bVar16 = param_5[0xf];
  bVar17 = param_4[0x10];
  bVar18 = param_5[0x10];
  bVar19 = param_4[0x11];
  bVar20 = param_5[0x11];
  bVar21 = param_4[0x12];
  bVar22 = param_5[0x12];
  bVar23 = param_4[0x13];
  bVar24 = param_5[0x13];
  bVar25 = param_4[0x14];
  bVar26 = param_5[0x14];
  bVar27 = param_4[0x15];
  bVar28 = param_5[0x15];
  bVar29 = param_4[0x16];
  bVar30 = param_5[0x16];
  bVar31 = param_4[0x17];
  bVar32 = param_5[0x17];
  bVar33 = param_4[0x18];
  bVar34 = param_5[0x18];
  bVar35 = param_4[0x19];
  bVar36 = param_5[0x19];
  bVar37 = param_4[0x1a];
  bVar38 = param_5[0x1a];
  bVar39 = param_4[0x1b];
  bVar40 = param_5[0x1b];
  bVar41 = param_4[0x1c];
  bVar42 = param_5[0x1c];
  bVar43 = param_4[0x1d];
  bVar44 = param_5[0x1d];
  bVar45 = param_4[0x1e];
  bVar46 = param_5[0x1e];
  bVar47 = param_4[0x1f];
  bVar48 = param_5[0x1f];
  uVar54 = CONCAT17(param_5[7] ^ param_4[7],
                    CONCAT16(param_5[6] ^ param_4[6],
                             CONCAT15(param_5[5] ^ param_4[5],
                                      CONCAT14(param_5[4] ^ param_4[4],
                                               CONCAT13(param_5[3] ^ param_4[3],
                                                        CONCAT12(param_5[2] ^ param_4[2],
                                                                 CONCAT11(param_5[1] ^ param_4[1],
                                                                          *param_5 ^ *param_4)))))))
  ;
  uVar51 = DAT_10009ecd0 ^ DAT_10009ecc8;
  uVar52 = DAT_10009ece0 ^ DAT_10009ecd8;
  uVar53 = DAT_10009ecf0 ^ DAT_10009ece8;
  do {
    uVar54 = uVar51 + uVar54;
    uVar55 = (uVar54 ^ uVar54 >> 0x1e) * uVar52;
    uVar55 = (uVar55 ^ uVar55 >> 0x1b) * uVar53;
    uVar55 = CONCAT17(bVar16 ^ bVar15,
                      CONCAT16(bVar14 ^ bVar13,
                               CONCAT15(bVar12 ^ bVar11,
                                        CONCAT14(bVar10 ^ bVar9,
                                                 CONCAT13(bVar8 ^ bVar7,
                                                          CONCAT12(bVar6 ^ bVar5,
                                                                   CONCAT11(bVar4 ^ bVar3,
                                                                            bVar2 ^ bVar1))))))) ^
             uVar55 >> 0x1f ^ uVar55;
    uVar55 = CONCAT17(bVar32 ^ bVar31,
                      CONCAT16(bVar30 ^ bVar29,
                               CONCAT15(bVar28 ^ bVar27,
                                        CONCAT14(bVar26 ^ bVar25,
                                                 CONCAT13(bVar24 ^ bVar23,
                                                          CONCAT12(bVar22 ^ bVar21,
                                                                   CONCAT11(bVar20 ^ bVar19,
                                                                            bVar18 ^ bVar17))))))) ^
             (uVar55 >> 0x33 | uVar55 << 0xd);
    uVar56 = CONCAT17(bVar48 ^ bVar47,
                      CONCAT16(bVar46 ^ bVar45,
                               CONCAT15(bVar44 ^ bVar43,
                                        CONCAT14(bVar42 ^ bVar41,
                                                 CONCAT13(bVar40 ^ bVar39,
                                                          CONCAT12(bVar38 ^ bVar37,
                                                                   CONCAT11(bVar36 ^ bVar35,
                                                                            bVar34 ^ bVar33))))))) ^
             (uVar55 >> 0x2f | uVar55 << 0x11);
    *(byte *)(param_1 + uVar50) = *(byte *)(param_2 + uVar50) ^ (byte)uVar56;
    uVar55 = uVar50 + 1;
    if (uVar55 < param_3) {
      *(byte *)(param_1 + uVar55) = *(byte *)(param_2 + uVar55) ^ (byte)(uVar56 >> 8);
      uVar55 = uVar50 + 2;
      if (uVar55 < param_3) {
        *(byte *)(param_1 + uVar55) = *(byte *)(param_2 + uVar55) ^ (byte)(uVar56 >> 0x10);
        uVar55 = uVar50 + 3;
        if (uVar55 < param_3) {
          *(byte *)(param_1 + uVar55) = *(byte *)(param_2 + uVar55) ^ (byte)(uVar56 >> 0x18);
          uVar55 = uVar50 + 4;
          if (uVar55 < param_3) {
            *(byte *)(param_1 + uVar55) = *(byte *)(param_2 + uVar55) ^ (byte)(uVar56 >> 0x20);
            uVar55 = uVar50 + 5;
            if (uVar55 < param_3) {
              *(byte *)(param_1 + uVar55) = *(byte *)(param_2 + uVar55) ^ (byte)(uVar56 >> 0x28);
              uVar55 = uVar50 + 6;
              if (uVar55 < param_3) {
                *(byte *)(param_1 + uVar55) = *(byte *)(param_2 + uVar55) ^ (byte)(uVar56 >> 0x30);
                uVar55 = uVar50 + 7;
                if (uVar55 < param_3) {
                  *(byte *)(param_1 + uVar55) = *(byte *)(param_2 + uVar55) ^ (byte)(uVar56 >> 0x38)
                  ;
                  bVar49 = uVar50 + 8 < param_3;
                  uVar50 = uVar50 + 8;
                }
                else {
                  bVar49 = false;
                  uVar50 = uVar55;
                }
              }
              else {
                bVar49 = false;
                uVar50 = uVar55;
              }
            }
            else {
              bVar49 = false;
              uVar50 = uVar55;
            }
          }
          else {
            bVar49 = false;
            uVar50 = uVar55;
          }
        }
        else {
          bVar49 = false;
          uVar50 = uVar55;
        }
      }
      else {
        bVar49 = false;
        uVar50 = uVar55;
      }
    }
    else {
      bVar49 = false;
      uVar50 = uVar55;
    }
  } while (bVar49);
  return;
}

