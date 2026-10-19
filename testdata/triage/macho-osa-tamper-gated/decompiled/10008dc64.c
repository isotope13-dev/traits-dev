// FUN_10008dc64 @ 10008dc64

/* WARNING: Removing unreachable block (ram,0x00010008dd48) */
/* WARNING: Removing unreachable block (ram,0x00010008dcc8) */
/* WARNING: Removing unreachable block (ram,0x00010008ddd0) */
/* WARNING: Removing unreachable block (ram,0x00010008de60) */

void FUN_10008dc64(void)

{
  undefined1 *puVar1;
  char cVar2;
  byte bVar3;
  byte bVar4;
  int iVar5;
  uint uVar6;
  uint uVar7;
  uint uVar8;
  uint uVar9;
  uint uVar10;
  time_t tVar11;
  ulong uVar12;
  long lVar13;
  long lVar14;
  long lVar15;
  undefined1 *puVar16;
  long lVar17;
  undefined8 uVar18;
  long lVar19;
  undefined8 local_11c;
  undefined4 local_114;
  byte local_110;
  byte local_10f;
  byte local_10e;
  byte local_10d;
  byte local_10c;
  byte local_10b;
  byte local_10a;
  byte local_109;
  byte local_108;
  byte local_107;
  byte local_106;
  byte local_105;
  byte local_104;
  byte local_103;
  byte local_102;
  byte local_101;
  byte local_100;
  byte local_ff;
  byte local_fe;
  byte local_fd;
  byte local_fc;
  byte local_fb;
  byte local_fa;
  byte local_f9;
  byte local_f8;
  byte local_f7;
  byte local_f6;
  byte local_f5;
  undefined4 local_f4;
  byte local_f0;
  byte local_ef;
  byte local_ee;
  byte local_ed;
  byte local_ec;
  byte local_eb;
  byte local_ea;
  byte local_e9;
  byte local_e8;
  undefined2 local_e7;
  byte local_e5;
  byte local_e4;
  byte local_e3;
  byte local_e2;
  byte local_e1;
  byte local_e0;
  byte local_df;
  byte local_de;
  byte local_dd;
  byte local_dc;
  byte local_db;
  byte local_da;
  byte local_d9;
  byte local_d8;
  byte local_d7;
  byte local_d6;
  byte local_d5;
  byte local_d4;
  byte local_d3;
  byte local_d2;
  byte local_d1;
  undefined4 local_d0;
  byte local_cc;
  byte local_cb;
  byte local_ca;
  byte local_c9;
  byte local_c8;
  byte local_c7;
  undefined2 local_c6;
  byte local_c4;
  byte local_c3;
  byte local_c2;
  byte local_c1;
  byte local_c0;
  byte local_bf;
  byte local_be;
  byte local_bd;
  byte local_bc;
  byte local_bb;
  byte local_ba;
  byte local_b9;
  byte local_b8;
  byte local_b7;
  byte local_b6;
  byte local_b5;
  byte local_b4;
  byte local_b3;
  byte local_b2;
  byte local_b1;
  undefined8 local_b0;
  undefined8 local_a8;
  undefined8 local_a0;
  undefined8 local_98;
  undefined8 local_90;
  undefined8 local_88;
  undefined8 local_80;
  undefined8 local_78;
  long local_70;
  
  local_70 = *(long *)PTR____stack_chk_guard_100102830;
  local_90 = 0;
  local_88 = 0;
  local_80 = 0;
  local_78 = 0;
  local_b0 = 0;
  local_a8 = 0;
  local_a0 = 0;
  local_98 = 0;
  local_f4 = 0xf;
  local_d0 = 0x30;
  lVar15 = 0;
  puVar16 = (undefined1 *)0x0;
  uVar10 = 7;
LAB_10008df50:
  do {
    while( true ) {
      while( true ) {
        while( true ) {
          while (uVar10 < 5) {
            if (uVar10 < 2) {
              if (uVar10 != 0) {
                local_b0 = 0;
                local_a8 = 0;
                local_a0 = 0;
                local_98 = 0;
                local_90 = 0;
                local_88 = 0;
                local_80 = 0;
                local_78 = 0;
                puVar1 = puVar16;
                if (puVar16 != (undefined1 *)0x0) {
                  for (; lVar15 != 0; lVar15 = lVar15 + -1) {
                    *puVar1 = 0;
                    puVar1 = puVar1 + 1;
                  }
                  FUN_100093d28(puVar16);
                }
                if (*(long *)PTR____stack_chk_guard_100102830 == local_70) {
                  return;
                }
                    /* WARNING: Subroutine does not return */
                ___stack_chk_fail();
              }
              local_11c = FUN_10008f23c();
              local_f0 = DAT_1000a00f8 ^ DAT_1000a00d8;
              local_ee = DAT_1000a00fa ^ DAT_1000a00da;
              local_ec = DAT_1000a00fc ^ DAT_1000a00dc;
              local_ea = DAT_1000a00fe ^ DAT_1000a00de;
              local_e8 = DAT_1000a0100 ^ DAT_1000a00e0;
              local_e4 = DAT_1000a0104 ^ DAT_1000a00e4;
              local_e2 = DAT_1000a0106 ^ DAT_1000a00e6;
              local_e0 = DAT_1000a0108 ^ DAT_1000a00e8;
              local_de = DAT_1000a010a ^ DAT_1000a00ea;
              local_dc = DAT_1000a010c ^ DAT_1000a00ec;
              local_da = DAT_1000a010e ^ DAT_1000a00ee;
              local_d8 = DAT_1000a0110 ^ DAT_1000a00f0;
              local_d6 = DAT_1000a0112 ^ DAT_1000a00f2;
              local_f4._0_2_ = CONCAT11(DAT_1000a00f5 ^ DAT_1000a00d5,DAT_1000a00f4 ^ DAT_1000a00d4)
              ;
              local_f4 = CONCAT13(DAT_1000a00f7 ^ DAT_1000a00d7,
                                  CONCAT12(DAT_1000a00f6 ^ DAT_1000a00d6,(undefined2)local_f4));
              local_ef = DAT_1000a00f9 ^ DAT_1000a00d9;
              local_ed = DAT_1000a00fb ^ DAT_1000a00db;
              local_eb = DAT_1000a00fd ^ DAT_1000a00dd;
              local_e9 = DAT_1000a00ff ^ DAT_1000a00df;
              local_e7 = CONCAT11(DAT_1000a0102 ^ DAT_1000a00e2,DAT_1000a0101 ^ DAT_1000a00e1);
              local_e5 = DAT_1000a0103 ^ DAT_1000a00e3;
              local_e3 = DAT_1000a0105 ^ DAT_1000a00e5;
              local_e1 = DAT_1000a0107 ^ DAT_1000a00e7;
              local_df = DAT_1000a0109 ^ DAT_1000a00e9;
              local_dd = DAT_1000a010b ^ DAT_1000a00eb;
              local_db = DAT_1000a010d ^ DAT_1000a00ed;
              local_d9 = DAT_1000a010f ^ DAT_1000a00ef;
              local_d7 = DAT_1000a0111 ^ DAT_1000a00f1;
              local_d5 = DAT_1000a0113 ^ DAT_1000a00f3;
              FUN_10009380c(&local_11c,8,&local_f4,0x20,&DAT_10009e8c8,0x12,&local_90,0x20);
              local_f4 = 0;
              local_f0 = 0;
              local_ef = 0;
              local_ee = 0;
              local_ed = 0;
              local_ec = 0;
              local_eb = 0;
              local_ea = 0;
              local_e9 = 0;
              local_e8 = 0;
              local_e7 = 0;
              local_e5 = 0;
              local_e4 = 0;
              local_e3 = 0;
              local_e2 = 0;
              local_e1 = 0;
              local_e0 = 0;
              local_df = 0;
              local_de = 0;
              local_dd = 0;
              local_dc = 0;
              local_db = 0;
              local_da = 0;
              local_d9 = 0;
              local_d8 = 0;
              local_d7 = 0;
              local_d6 = 0;
              local_d5 = 0;
              lVar19 = FUN_1000937f8(0x110);
              if (lVar19 == 0) {
                uVar10 = 1;
              }
              else {
                lVar14 = 0;
                lVar17 = 0;
                while( true ) {
                  local_d0 = CONCAT13(DAT_1000a0161 ^ DAT_1000a0157,
                                      CONCAT12(DAT_1000a0160 ^ DAT_1000a0156,
                                               CONCAT11(DAT_1000a015f ^ DAT_1000a0155,
                                                        DAT_1000a015e ^ DAT_1000a0154)));
                  local_cc = DAT_1000a0162 ^ DAT_1000a0158;
                  local_cb = DAT_1000a0163 ^ DAT_1000a0159;
                  local_ca = DAT_1000a0164 ^ DAT_1000a015a;
                  local_c9 = DAT_1000a0165 ^ DAT_1000a015b;
                  local_c8 = DAT_1000a0166 ^ DAT_1000a015c;
                  local_c7 = DAT_1000a0167 ^ DAT_1000a015d;
                  local_c6 = 0;
                  local_c4 = 0;
                  local_c3 = (byte)lVar14;
                  FUN_10009380c(&local_90,0x20,0,0,&local_d0,0xe,&local_114,0xc);
                  cVar2 = (&DAT_10009e8da)[lVar14];
                  puVar1 = (undefined1 *)(lVar19 + lVar17);
                  if (cVar2 != '7') {
                    puVar1 = &DAT_100105ccc;
                  }
                  uVar18 = (&DAT_10009e8e0)[lVar14];
                  FUN_100093a80((&PTR_s_G5Zi4OXnzG_mi_Sf5kyAs1nXMGikd78M_1001027e0)[lVar14],
                                &DAT_100104e6e,uVar18);
                  uVar12 = FUN_100093c00(&local_90,&local_114,&DAT_100104e6e,uVar18,
                                         (&PTR_DAT_100102808)[lVar14],puVar1);
                  if ((uVar12 & 1) == 0) break;
                  if (cVar2 == '7') {
                    lVar13 = (&DAT_10009e8e0)[lVar14];
                  }
                  else {
                    lVar13 = 0;
                  }
                  lVar17 = lVar13 + lVar17;
                  lVar14 = lVar14 + 1;
                  if (lVar14 == 5) goto LAB_10008efb4;
                }
                lVar14 = 0;
                do {
                  *(undefined1 *)(lVar19 + lVar14) = 0;
                  lVar14 = lVar14 + 1;
                } while (lVar14 != 0x110);
                FUN_100093d28(lVar19);
                uVar10 = 1;
              }
            }
            else if (uVar10 == 2) {
              uVar10 = FUN_10008f23c();
              iVar5 = FUN_10008f254();
              if (iVar5 == 0) {
                uVar6 = FUN_10008f4b0();
                uVar7 = FUN_100090a2c();
                uVar8 = FUN_100092114();
                uVar9 = FUN_100092ba8();
                uVar10 = uVar9 ^ uVar10 ^ (uVar7 ^ uVar6 ^ uVar8) & 0xffff;
              }
              lVar19 = FUN_100092ecc();
              FUN_100093050(&local_d0);
              bVar3 = (byte)local_d0;
              bVar4 = local_d0._2_1_;
              uVar10 = CONCAT13(DAT_1000a0037 ^ local_d0._3_1_,
                                CONCAT12(DAT_1000a0036 ^ local_d0._2_1_,
                                         CONCAT11(DAT_1000a0035 ^ local_d0._1_1_,
                                                  DAT_1000a0034 ^ (byte)local_d0))) ^ uVar10;
              lVar14 = FUN_100092ecc();
              uVar6 = uVar10 ^ 0x620dc775;
              if ((ulong)(lVar14 - lVar19) < 0x2faf081) {
                uVar6 = uVar10;
              }
              uVar10 = (uVar6 & 0xff00ff00) >> 8 | (uVar6 & 0xff00ff) << 8;
              local_f4 = uVar10 >> 0x10 | uVar10 << 0x10;
              local_f0 = DAT_1000a0034 ^ bVar3;
              local_ee = DAT_1000a0036 ^ bVar4;
              local_ec = DAT_1000a0038 ^ local_cc;
              local_ea = DAT_1000a003a ^ local_ca;
              local_e8 = DAT_1000a003c ^ local_c8;
              local_e4 = DAT_1000a0040 ^ local_c4;
              local_e2 = DAT_1000a0042 ^ local_c2;
              local_e0 = DAT_1000a0044 ^ local_c0;
              local_de = DAT_1000a0046 ^ local_be;
              local_dc = DAT_1000a0048 ^ local_bc;
              local_da = DAT_1000a004a ^ local_ba;
              local_d8 = DAT_1000a004c ^ local_b8;
              local_d6 = DAT_1000a004e ^ local_b6;
              local_d4 = DAT_1000a0050 ^ local_b4;
              local_d2 = DAT_1000a0052 ^ local_b2;
              local_ef = DAT_1000a0035 ^ local_d0._1_1_;
              local_ed = DAT_1000a0037 ^ local_d0._3_1_;
              local_eb = DAT_1000a0039 ^ local_cb;
              local_e9 = DAT_1000a003b ^ local_c9;
              local_e7 = CONCAT11(DAT_1000a003e ^ (byte)local_c6,DAT_1000a003d ^ local_c7);
              local_e5 = DAT_1000a003f ^ local_c6._1_1_;
              local_e3 = DAT_1000a0041 ^ local_c3;
              local_e1 = DAT_1000a0043 ^ local_c1;
              local_df = DAT_1000a0045 ^ local_bf;
              local_dd = DAT_1000a0047 ^ local_bd;
              local_db = DAT_1000a0049 ^ local_bb;
              local_d9 = DAT_1000a004b ^ local_b9;
              local_d7 = DAT_1000a004d ^ local_b7;
              local_d5 = DAT_1000a004f ^ local_b5;
              local_d3 = DAT_1000a0051 ^ local_b3;
              local_d1 = DAT_1000a0053 ^ local_b1;
              local_114 = CONCAT13(DAT_1000a0137 ^ DAT_1000a0117,
                                   CONCAT12(DAT_1000a0136 ^ DAT_1000a0116,
                                            CONCAT11(DAT_1000a0135 ^ DAT_1000a0115,
                                                     DAT_1000a0134 ^ DAT_1000a0114)));
              local_110 = DAT_1000a0138 ^ DAT_1000a0118;
              local_10f = DAT_1000a0139 ^ DAT_1000a0119;
              local_10e = DAT_1000a013a ^ DAT_1000a011a;
              local_10d = DAT_1000a013b ^ DAT_1000a011b;
              local_10c = DAT_1000a013c ^ DAT_1000a011c;
              local_10b = DAT_1000a013d ^ DAT_1000a011d;
              local_10a = DAT_1000a013e ^ DAT_1000a011e;
              local_109 = DAT_1000a013f ^ DAT_1000a011f;
              local_108 = DAT_1000a0140 ^ DAT_1000a0120;
              local_107 = DAT_1000a0141 ^ DAT_1000a0121;
              local_106 = DAT_1000a0142 ^ DAT_1000a0122;
              local_105 = DAT_1000a0143 ^ DAT_1000a0123;
              local_104 = DAT_1000a0144 ^ DAT_1000a0124;
              local_103 = DAT_1000a0145 ^ DAT_1000a0125;
              local_102 = DAT_1000a0146 ^ DAT_1000a0126;
              local_101 = DAT_1000a0147 ^ DAT_1000a0127;
              local_100 = DAT_1000a0148 ^ DAT_1000a0128;
              local_ff = DAT_1000a0149 ^ DAT_1000a0129;
              local_fe = DAT_1000a014a ^ DAT_1000a012a;
              local_fd = DAT_1000a014b ^ DAT_1000a012b;
              local_fc = DAT_1000a014c ^ DAT_1000a012c;
              local_fb = DAT_1000a014d ^ DAT_1000a012d;
              local_fa = DAT_1000a014e ^ DAT_1000a012e;
              local_f9 = DAT_1000a014f ^ DAT_1000a012f;
              local_f8 = DAT_1000a0150 ^ DAT_1000a0130;
              local_f7 = DAT_1000a0151 ^ DAT_1000a0131;
              local_f6 = DAT_1000a0152 ^ DAT_1000a0132;
              local_f5 = DAT_1000a0153 ^ DAT_1000a0133;
              FUN_1000933b8(&local_f4,&local_114,&local_b0);
              local_114 = 0;
              local_110 = 0;
              local_10f = 0;
              local_10e = 0;
              local_10d = 0;
              local_10c = 0;
              local_10b = 0;
              local_10a = 0;
              local_109 = 0;
              local_108 = 0;
              local_107 = 0;
              local_106 = 0;
              local_105 = 0;
              local_104 = 0;
              local_103 = 0;
              local_102 = 0;
              local_101 = 0;
              local_100 = 0;
              local_ff = 0;
              local_fe = 0;
              local_fd = 0;
              local_fc = 0;
              local_fb = 0;
              local_fa = 0;
              local_f9 = 0;
              local_f8 = 0;
              local_f7 = 0;
              local_f6 = 0;
              local_f5 = 0;
              local_f4 = 0;
              local_f0 = 0;
              local_ef = 0;
              local_ee = 0;
              local_ed = 0;
              local_ec = 0;
              local_eb = 0;
              local_ea = 0;
              local_e9 = 0;
              local_e8 = 0;
              local_e7 = 0;
              local_e5 = 0;
              local_e4 = 0;
              local_e3 = 0;
              local_e2 = 0;
              local_e1 = 0;
              local_e0 = 0;
              local_df = 0;
              local_de = 0;
              local_dd = 0;
              local_dc = 0;
              local_db = 0;
              local_da = 0;
              local_d9 = 0;
              local_d8 = 0;
              local_d7 = 0;
              local_d6 = 0;
              local_d5 = 0;
              local_d4 = 0;
              local_d3 = 0;
              local_d2 = 0;
              local_d1 = 0;
              uVar10 = 8;
            }
            else {
              uVar12 = FUN_100093d3c(puVar16,lVar15,&DAT_1000a05e1,&DAT_1000a0601);
              lVar19 = lVar15;
              puVar1 = puVar16;
              if ((uVar12 & 1) == 0) {
                for (; lVar19 != 0; lVar19 = lVar19 + -1) {
                  *puVar1 = 0;
                  puVar1 = puVar1 + 1;
                }
                FUN_100093d28(puVar16);
                puVar16 = (undefined1 *)0x0;
                uVar10 = 1;
              }
              else {
                uVar10 = 5;
              }
            }
          }
          if (6 < uVar10) break;
          if (uVar10 == 5) {
            FUN_100096f2c();
            FUN_1000989bc(&local_b0);
            local_b0 = 0;
            local_a8 = 0;
            local_a0 = 0;
            local_98 = 0;
            FUN_100093fdc(puVar16,lVar15,&DAT_1000a05e1,&DAT_1000a0601);
            FUN_100096f2c();
            uVar10 = 1;
          }
          else {
            uVar10 = _getpid();
            tVar11 = _time((time_t *)0x0);
            local_f4 = uVar10 ^ (uint)tVar11 ^ 0x756ca5e1;
            local_d0 = SUB84(&local_f4,0);
            local_114 = 0x803c1a47;
            uVar10 = 1;
          }
        }
        if (uVar10 != 7) break;
        uVar10 = 0;
        local_f4 = 0x68e7e1aa;
      }
      puVar16 = (undefined1 *)FUN_1000937f8(0x3fe14);
      if (puVar16 != (undefined1 *)0x0) break;
      uVar10 = 1;
      lVar15 = 0x3fe14;
    }
    lVar15 = 0;
    lVar19 = 0;
    local_114 = CONCAT31(local_114._1_3_,200);
    local_11c = CONCAT71(local_11c._1_7_,0x6f);
    while( true ) {
      local_f4._0_2_ = CONCAT11(DAT_1000a0176 ^ DAT_1000a0169,DAT_1000a0175 ^ DAT_1000a0168);
      local_f4 = CONCAT13(DAT_1000a0178 ^ DAT_1000a016b,
                          CONCAT12(DAT_1000a0177 ^ DAT_1000a016a,(undefined2)local_f4));
      local_f0 = DAT_1000a0179 ^ DAT_1000a016c;
      local_ef = DAT_1000a017a ^ DAT_1000a016d;
      local_ee = DAT_1000a017b ^ DAT_1000a016e;
      local_ed = DAT_1000a017c ^ DAT_1000a016f;
      local_ec = DAT_1000a017d ^ DAT_1000a0170;
      local_eb = DAT_1000a017e ^ DAT_1000a0171;
      local_ea = DAT_1000a017f ^ DAT_1000a0172;
      local_e9 = DAT_1000a0180 ^ DAT_1000a0173;
      local_e8 = DAT_1000a0181 ^ DAT_1000a0174;
      local_e7 = 0;
      local_e5 = 0;
      local_e4 = (byte)lVar15;
      FUN_10009380c(&local_b0,0x20,0,0,&local_f4,0x11,&local_d0,0xc);
      cVar2 = (&DAT_10009e558)[lVar15];
      puVar1 = puVar16 + lVar19;
      if (cVar2 != '7') {
        puVar1 = &DAT_100104efe;
      }
      uVar18 = (&DAT_10009e5c0)[lVar15];
      FUN_100093a80((&PTR_s_Srz8259kwmla2BSmUNWZRNECJ34CANoL_1001021d0)[lVar15],&DAT_1001040a0,
                    uVar18);
      uVar12 = FUN_100093c00(&local_b0,&local_d0,&DAT_1001040a0,uVar18,(&PTR_DAT_1001024d8)[lVar15],
                             puVar1);
      if ((uVar12 & 1) == 0) break;
      if (cVar2 == '7') {
        lVar14 = (&DAT_10009e5c0)[lVar15];
      }
      else {
        lVar14 = 0;
      }
      lVar19 = lVar14 + lVar19;
      lVar15 = lVar15 + 1;
      if (lVar15 == 0x61) goto LAB_10008ef48;
    }
    lVar15 = 0;
    do {
      puVar16[lVar15] = 0;
      lVar15 = lVar15 + 1;
    } while (lVar15 != 0x3fe14);
    FUN_100093d28(puVar16);
    puVar16 = (undefined1 *)0x0;
    uVar10 = 1;
    lVar15 = 0x3fe14;
  } while( true );
LAB_10008efb4:
  lVar14 = 0;
  do {
    (&DAT_100104e6e)[lVar14] = 0;
    lVar14 = lVar14 + 1;
  } while (lVar14 != 0x90);
  lVar14 = 0;
  do {
    (&DAT_100105ccc)[lVar14] = 0;
    lVar14 = lVar14 + 1;
  } while (lVar14 != 0x90);
  iVar5 = FUN_100093fdc(lVar19,0x110,&DAT_1000a05a1,&DAT_1000a05c1);
  lVar14 = 0;
  do {
    *(undefined1 *)(lVar19 + lVar14) = 0;
    lVar14 = lVar14 + 1;
  } while (lVar14 != 0x110);
  FUN_100093d28(lVar19);
  local_90 = 0;
  local_88 = 0;
  local_80 = 0;
  local_78 = 0;
  uVar10 = 1;
  if (iVar5 == 0) {
    uVar10 = 2;
  }
  goto LAB_10008df50;
LAB_10008ef48:
  lVar15 = 0;
  do {
    (&DAT_1001040a0)[lVar15] = 0;
    lVar15 = lVar15 + 1;
  } while (lVar15 != 0xdce);
  lVar15 = 0;
  do {
    (&DAT_100104efe)[lVar15] = 0;
    lVar15 = lVar15 + 1;
  } while (lVar15 != 0xdce);
  uVar10 = 4;
  lVar15 = 0x3fe14;
  goto LAB_10008df50;
}

