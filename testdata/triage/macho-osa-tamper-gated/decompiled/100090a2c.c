// FUN_100090a2c @ 100090a2c

/* WARNING: Removing unreachable block (ram,0x000100091388) */
/* WARNING: Removing unreachable block (ram,0x000100090f88) */
/* WARNING: Removing unreachable block (ram,0x0001000919fc) */

uint FUN_100090a2c(void)

{
  uint uVar1;
  byte bVar2;
  code *pcVar3;
  bool bVar4;
  int iVar5;
  ulong uVar6;
  byte *pbVar7;
  char *pcVar8;
  char cVar9;
  char *pcVar10;
  ulong uVar11;
  uint uVar12;
  undefined *puVar13;
  char *pcVar14;
  long lVar15;
  char *pcVar16;
  long lVar17;
  undefined8 local_6b0;
  int local_6a8 [5];
  undefined1 local_691;
  ulong local_690;
  undefined1 local_683;
  undefined1 local_682;
  undefined1 local_681;
  undefined1 local_680;
  undefined1 local_67f;
  undefined1 local_67e;
  undefined1 local_67d;
  undefined1 local_67c;
  undefined1 local_67b;
  undefined1 local_67a;
  undefined1 local_679;
  undefined8 local_678;
  undefined1 local_670;
  undefined1 local_66f;
  undefined1 local_66e;
  undefined1 local_66d;
  undefined1 local_66c;
  undefined1 local_66b;
  undefined1 local_66a;
  undefined1 local_669;
  undefined1 local_668;
  undefined8 local_660;
  undefined1 local_658;
  undefined1 local_657;
  undefined1 local_656;
  undefined1 local_655;
  undefined1 local_654;
  undefined1 local_653;
  undefined1 local_652;
  undefined1 local_651;
  undefined1 local_650;
  undefined1 local_64f;
  undefined1 local_64e;
  undefined1 local_64d;
  undefined8 local_648;
  undefined8 local_640;
  undefined8 local_638;
  undefined8 local_630;
  undefined8 local_628;
  undefined8 local_620;
  undefined8 local_618;
  undefined8 local_610;
  code *local_608;
  undefined1 local_600;
  char local_5f8 [1416];
  long local_70;
  
  local_70 = *(long *)PTR____stack_chk_guard_100102830;
  local_679 = 0x86;
  local_67a = 0x17;
  if ((DAT_100106208 == (code *)0x0) &&
     (DAT_100106208 = (code *)FUN_10009b6b4(0x35d428ca588487de), DAT_100106208 == (code *)0x0)) {
    uVar12 = 0;
  }
  else {
    pcVar3 = DAT_100106208;
    pcVar14 = (char *)0x0;
    lVar15 = 0;
    local_5f8[0x188] = 0;
    local_5f8[0x148] = 0;
    do {
      FUN_10009de8c(&DAT_10009f158 + lVar15 * 0x18,(&DAT_10009f1a0)[lVar15],0x9d,local_5f8 + 0x120);
      FUN_10009de8c(&DAT_10009f1a3 + lVar15 * 0x17,(&DAT_10009f1e8)[lVar15],0x9d,local_5f8 + 0x100);
      local_5f8[0xf0] = '\0';
      local_5f8[0xf1] = '\0';
      local_5f8[0xf2] = '\0';
      local_5f8[0xf3] = '\0';
      local_5f8[0xf4] = '\0';
      local_5f8[0xf5] = '\0';
      local_5f8[0xf6] = '\0';
      local_5f8[0xf7] = '\0';
      local_5f8[0xf8] = '\0';
      local_5f8[0xf9] = '\0';
      local_5f8[0xfa] = '\0';
      local_5f8[0xfb] = '\0';
      local_5f8[0xfc] = '\0';
      local_5f8[0xfd] = '\0';
      local_5f8[0xfe] = '\0';
      local_5f8[0xff] = '\0';
      local_5f8[0xe0] = '\0';
      local_5f8[0xe1] = '\0';
      local_5f8[0xe2] = '\0';
      local_5f8[0xe3] = '\0';
      local_5f8[0xe4] = '\0';
      local_5f8[0xe5] = '\0';
      local_5f8[0xe6] = '\0';
      local_5f8[0xe7] = '\0';
      local_5f8[0xe8] = '\0';
      local_5f8[0xe9] = '\0';
      local_5f8[0xea] = '\0';
      local_5f8[0xeb] = '\0';
      local_5f8[0xec] = '\0';
      local_5f8[0xed] = '\0';
      local_5f8[0xee] = '\0';
      local_5f8[0xef] = '\0';
      local_5f8[0xd0] = '\0';
      local_5f8[0xd1] = '\0';
      local_5f8[0xd2] = '\0';
      local_5f8[0xd3] = '\0';
      local_5f8[0xd4] = '\0';
      local_5f8[0xd5] = '\0';
      local_5f8[0xd6] = '\0';
      local_5f8[0xd7] = '\0';
      local_5f8[0xd8] = '\0';
      local_5f8[0xd9] = '\0';
      local_5f8[0xda] = '\0';
      local_5f8[0xdb] = '\0';
      local_5f8[0xdc] = '\0';
      local_5f8[0xdd] = '\0';
      local_5f8[0xde] = '\0';
      local_5f8[0xdf] = '\0';
      local_5f8[0xc0] = '\0';
      local_5f8[0xc1] = '\0';
      local_5f8[0xc2] = '\0';
      local_5f8[0xc3] = '\0';
      local_5f8[0xc4] = '\0';
      local_5f8[0xc5] = '\0';
      local_5f8[0xc6] = '\0';
      local_5f8[199] = '\0';
      local_5f8[200] = '\0';
      local_5f8[0xc9] = '\0';
      local_5f8[0xca] = '\0';
      local_5f8[0xcb] = '\0';
      local_5f8[0xcc] = '\0';
      local_5f8[0xcd] = '\0';
      local_5f8[0xce] = '\0';
      local_5f8[0xcf] = '\0';
      local_5f8[0xb0] = '\0';
      local_5f8[0xb1] = '\0';
      local_5f8[0xb2] = '\0';
      local_5f8[0xb3] = '\0';
      local_5f8[0xb4] = '\0';
      local_5f8[0xb5] = '\0';
      local_5f8[0xb6] = '\0';
      local_5f8[0xb7] = '\0';
      local_5f8[0xb8] = '\0';
      local_5f8[0xb9] = '\0';
      local_5f8[0xba] = '\0';
      local_5f8[0xbb] = '\0';
      local_5f8[0xbc] = '\0';
      local_5f8[0xbd] = '\0';
      local_5f8[0xbe] = '\0';
      local_5f8[0xbf] = '\0';
      local_5f8[0xa0] = '\0';
      local_5f8[0xa1] = '\0';
      local_5f8[0xa2] = '\0';
      local_5f8[0xa3] = '\0';
      local_5f8[0xa4] = '\0';
      local_5f8[0xa5] = '\0';
      local_5f8[0xa6] = '\0';
      local_5f8[0xa7] = '\0';
      local_5f8[0xa8] = '\0';
      local_5f8[0xa9] = '\0';
      local_5f8[0xaa] = '\0';
      local_5f8[0xab] = '\0';
      local_5f8[0xac] = '\0';
      local_5f8[0xad] = '\0';
      local_5f8[0xae] = '\0';
      local_5f8[0xaf] = '\0';
      local_5f8[0x90] = '\0';
      local_5f8[0x91] = '\0';
      local_5f8[0x92] = '\0';
      local_5f8[0x93] = '\0';
      local_5f8[0x94] = '\0';
      local_5f8[0x95] = '\0';
      local_5f8[0x96] = '\0';
      local_5f8[0x97] = '\0';
      local_5f8[0x98] = '\0';
      local_5f8[0x99] = '\0';
      local_5f8[0x9a] = '\0';
      local_5f8[0x9b] = '\0';
      local_5f8[0x9c] = '\0';
      local_5f8[0x9d] = '\0';
      local_5f8[0x9e] = '\0';
      local_5f8[0x9f] = '\0';
      local_5f8[0x80] = '\0';
      local_5f8[0x81] = '\0';
      local_5f8[0x82] = '\0';
      local_5f8[0x83] = '\0';
      local_5f8[0x84] = '\0';
      local_5f8[0x85] = '\0';
      local_5f8[0x86] = '\0';
      local_5f8[0x87] = '\0';
      local_5f8[0x88] = '\0';
      local_5f8[0x89] = '\0';
      local_5f8[0x8a] = '\0';
      local_5f8[0x8b] = '\0';
      local_5f8[0x8c] = '\0';
      local_5f8[0x8d] = '\0';
      local_5f8[0x8e] = '\0';
      local_5f8[0x8f] = '\0';
      local_5f8[0x70] = '\0';
      local_5f8[0x71] = '\0';
      local_5f8[0x72] = '\0';
      local_5f8[0x73] = '\0';
      local_5f8[0x74] = '\0';
      local_5f8[0x75] = '\0';
      local_5f8[0x76] = '\0';
      local_5f8[0x77] = '\0';
      local_5f8[0x78] = '\0';
      local_5f8[0x79] = '\0';
      local_5f8[0x7a] = '\0';
      local_5f8[0x7b] = '\0';
      local_5f8[0x7c] = '\0';
      local_5f8[0x7d] = '\0';
      local_5f8[0x7e] = '\0';
      local_5f8[0x7f] = '\0';
      local_5f8[0x60] = '\0';
      local_5f8[0x61] = '\0';
      local_5f8[0x62] = '\0';
      local_5f8[99] = '\0';
      local_5f8[100] = '\0';
      local_5f8[0x65] = '\0';
      local_5f8[0x66] = '\0';
      local_5f8[0x67] = '\0';
      local_5f8[0x68] = '\0';
      local_5f8[0x69] = '\0';
      local_5f8[0x6a] = '\0';
      local_5f8[0x6b] = '\0';
      local_5f8[0x6c] = '\0';
      local_5f8[0x6d] = '\0';
      local_5f8[0x6e] = '\0';
      local_5f8[0x6f] = '\0';
      local_5f8[0x50] = '\0';
      local_5f8[0x51] = '\0';
      local_5f8[0x52] = '\0';
      local_5f8[0x53] = '\0';
      local_5f8[0x54] = '\0';
      local_5f8[0x55] = '\0';
      local_5f8[0x56] = '\0';
      local_5f8[0x57] = '\0';
      local_5f8[0x58] = '\0';
      local_5f8[0x59] = '\0';
      local_5f8[0x5a] = '\0';
      local_5f8[0x5b] = '\0';
      local_5f8[0x5c] = '\0';
      local_5f8[0x5d] = '\0';
      local_5f8[0x5e] = '\0';
      local_5f8[0x5f] = '\0';
      local_5f8[0x40] = '\0';
      local_5f8[0x41] = '\0';
      local_5f8[0x42] = '\0';
      local_5f8[0x43] = '\0';
      local_5f8[0x44] = '\0';
      local_5f8[0x45] = '\0';
      local_5f8[0x46] = '\0';
      local_5f8[0x47] = '\0';
      local_5f8[0x48] = '\0';
      local_5f8[0x49] = '\0';
      local_5f8[0x4a] = '\0';
      local_5f8[0x4b] = '\0';
      local_5f8[0x4c] = '\0';
      local_5f8[0x4d] = '\0';
      local_5f8[0x4e] = '\0';
      local_5f8[0x4f] = '\0';
      local_5f8[0x30] = '\0';
      local_5f8[0x31] = '\0';
      local_5f8[0x32] = '\0';
      local_5f8[0x33] = '\0';
      local_5f8[0x34] = '\0';
      local_5f8[0x35] = '\0';
      local_5f8[0x36] = '\0';
      local_5f8[0x37] = '\0';
      local_5f8[0x38] = '\0';
      local_5f8[0x39] = '\0';
      local_5f8[0x3a] = '\0';
      local_5f8[0x3b] = '\0';
      local_5f8[0x3c] = '\0';
      local_5f8[0x3d] = '\0';
      local_5f8[0x3e] = '\0';
      local_5f8[0x3f] = '\0';
      local_5f8[0x20] = '\0';
      local_5f8[0x21] = '\0';
      local_5f8[0x22] = '\0';
      local_5f8[0x23] = '\0';
      local_5f8[0x24] = '\0';
      local_5f8[0x25] = '\0';
      local_5f8[0x26] = '\0';
      local_5f8[0x27] = '\0';
      local_5f8[0x28] = '\0';
      local_5f8[0x29] = '\0';
      local_5f8[0x2a] = '\0';
      local_5f8[0x2b] = '\0';
      local_5f8[0x2c] = '\0';
      local_5f8[0x2d] = '\0';
      local_5f8[0x2e] = '\0';
      local_5f8[0x2f] = '\0';
      local_5f8[0x10] = '\0';
      local_5f8[0x11] = '\0';
      local_5f8[0x12] = '\0';
      local_5f8[0x13] = '\0';
      local_5f8[0x14] = '\0';
      local_5f8[0x15] = '\0';
      local_5f8[0x16] = '\0';
      local_5f8[0x17] = '\0';
      local_5f8[0x18] = '\0';
      local_5f8[0x19] = '\0';
      local_5f8[0x1a] = '\0';
      local_5f8[0x1b] = '\0';
      local_5f8[0x1c] = '\0';
      local_5f8[0x1d] = '\0';
      local_5f8[0x1e] = '\0';
      local_5f8[0x1f] = '\0';
      local_5f8[0] = '\0';
      local_5f8[1] = '\0';
      local_5f8[2] = '\0';
      local_5f8[3] = '\0';
      local_5f8[4] = '\0';
      local_5f8[5] = '\0';
      local_5f8[6] = '\0';
      local_5f8[7] = '\0';
      local_5f8[8] = '\0';
      local_5f8[9] = '\0';
      local_5f8[10] = '\0';
      local_5f8[0xb] = '\0';
      local_5f8[0xc] = '\0';
      local_5f8[0xd] = '\0';
      local_5f8[0xe] = '\0';
      local_5f8[0xf] = '\0';
      local_660 = 0x100;
      local_648 = 0x100;
      local_678 = 0;
      local_608 = pcVar3;
      iVar5 = (*pcVar3)(local_5f8 + 0x120,local_5f8,&local_648,0,0);
      local_5f8[0x120] = 0;
      local_5f8[0x121] = 0;
      local_5f8[0x122] = 0;
      local_5f8[0x123] = 0;
      local_5f8[0x124] = 0;
      local_5f8[0x125] = 0;
      local_5f8[0x126] = 0;
      local_5f8[0x127] = 0;
      local_5f8[0x128] = 0;
      local_5f8[0x129] = 0;
      local_5f8[0x12a] = 0;
      local_5f8[299] = 0;
      local_5f8[300] = 0;
      local_5f8[0x12d] = 0;
      local_5f8[0x12e] = 0;
      local_5f8[0x12f] = 0;
      local_5f8[0x130] = 0;
      local_5f8[0x131] = 0;
      local_5f8[0x132] = 0;
      local_5f8[0x133] = 0;
      local_5f8[0x134] = 0;
      local_5f8[0x135] = 0;
      local_5f8[0x136] = 0;
      local_5f8[0x137] = 0;
      local_5f8[0x138] = 0;
      local_5f8[0x139] = 0;
      local_5f8[0x13a] = 0;
      local_5f8[0x13b] = 0;
      local_5f8[0x13c] = 0;
      local_5f8[0x13d] = 0;
      local_5f8[0x13e] = 0;
      local_5f8[0x13f] = 0;
      local_5f8[0x140] = 0;
      local_5f8[0x141] = 0;
      local_5f8[0x142] = 0;
      local_5f8[0x143] = 0;
      local_5f8[0x144] = 0;
      local_5f8[0x145] = 0;
      local_5f8[0x146] = 0;
      local_5f8[0x147] = 0;
      if ((iVar5 == 0) && (local_648 != 0)) {
        if (0xff < local_648) {
          local_648 = 0xff;
        }
        local_5f8[local_648] = '\0';
        uVar6 = local_648 - 1;
        do {
          if (local_5f8[uVar6] != '\n' && local_5f8[uVar6] != '\0') {
            lVar17 = uVar6 + 1;
            goto LAB_100090d20;
          }
          local_648 = uVar6;
          local_5f8[uVar6] = '\0';
          uVar6 = uVar6 - 1;
        } while (uVar6 != 0xffffffffffffffff);
        lVar17 = 0;
LAB_100090d20:
        uVar6 = 0;
        while (uVar6 < 0x20) {
          pcVar8 = local_5f8 + uVar6 + 0x100;
          cVar9 = *pcVar8;
          pcVar16 = pcVar8;
          uVar11 = uVar6;
          if (cVar9 == '\0') break;
          while ((cVar9 != '\0' && (cVar9 != '|'))) {
            if (uVar11 == 0x1f) {
              bVar4 = false;
              uVar11 = 0x20;
              pcVar16 = local_5f8 + 0x120;
              goto LAB_100090d7c;
            }
            cVar9 = pcVar16[1];
            pcVar16 = pcVar16 + 1;
            uVar11 = uVar11 + 1;
          }
          bVar4 = true;
LAB_100090d7c:
          pcVar10 = pcVar14 + 2;
          if ((pcVar8 < pcVar16) && (pcVar10 < (char *)0x400)) {
            pcVar10 = pcVar16 + (~(ulong)(local_5f8 + 0x100) - uVar6);
            if ((char *)(0x3fd - (long)pcVar14) <= pcVar16 + (~(ulong)(local_5f8 + 0x100) - uVar6))
            {
              pcVar10 = (char *)(0x3fd - (long)pcVar14);
            }
            _memcpy(pcVar14 + (long)(local_5f8 + 0x188),pcVar8,(size_t)(pcVar10 + 1));
            pcVar14 = pcVar10 + 1 + (long)pcVar14;
            pcVar10 = pcVar14 + 2;
          }
          if ((lVar17 != 0) && (pcVar10 < (char *)0x400)) {
            uVar6 = lVar17 - 1U;
            if (0x3fdU - (long)pcVar14 <= lVar17 - 1U) {
              uVar6 = 0x3fdU - (long)pcVar14;
            }
            _memcpy(pcVar14 + (long)(local_5f8 + 0x188),local_5f8,uVar6 + 1);
            pcVar14 = pcVar14 + uVar6 + 1;
          }
          if (pcVar14 + 1 < (char *)0x400) {
            pcVar14[(long)(local_5f8 + 0x188)] = '\n';
            pcVar14 = pcVar14 + 1;
          }
          if ((!bVar4) || (uVar6 = uVar11 + 1, *pcVar16 != '|')) break;
        }
        lVar17 = 0;
        do {
          local_5f8[lVar17] = '\0';
          lVar17 = lVar17 + 1;
        } while (lVar17 != 0x100);
      }
      local_5f8[0x11f] = 0;
      local_5f8[0x11e] = 0;
      local_5f8[0x11d] = 0;
      local_5f8[0x11c] = 0;
      local_5f8[0x11b] = 0;
      local_5f8[0x11a] = 0;
      local_5f8[0x119] = 0;
      local_5f8[0x118] = 0;
      local_5f8[0x117] = 0;
      local_5f8[0x116] = 0;
      local_5f8[0x115] = 0;
      local_5f8[0x114] = 0;
      local_5f8[0x113] = 0;
      local_5f8[0x112] = 0;
      local_5f8[0x111] = 0;
      local_5f8[0x110] = 0;
      local_5f8[0x10f] = 0;
      local_5f8[0x10e] = 0;
      local_5f8[0x10d] = 0;
      local_5f8[0x10c] = 0;
      local_5f8[0x10b] = 0;
      local_5f8[0x10a] = 0;
      local_5f8[0x109] = 0;
      local_5f8[0x108] = 0;
      local_5f8[0x107] = 0;
      local_5f8[0x106] = 0;
      local_5f8[0x105] = 0;
      local_5f8[0x104] = 0;
      local_5f8[0x103] = 0;
      local_5f8[0x102] = 0;
      local_5f8[0x101] = 0;
      local_5f8[0x100] = 0;
      lVar15 = lVar15 + 1;
    } while (lVar15 != 3);
    local_67b = 0;
    local_67c = 0xf1;
    local_67d = 0xf3;
    local_67e = 0xc5;
    local_67f = 0x32;
    local_680 = 0x8e;
    local_681 = 0x62;
    local_682 = 0x34;
    local_683 = 0xdc;
    local_608 = (code *)0x6c65646f6d2e7768;
    local_600 = 0;
    local_618 = 0;
    local_610 = 0;
    local_628 = 0;
    local_620 = 0;
    local_638 = 0;
    local_630 = 0;
    local_648 = 0;
    local_640 = 0;
    local_690 = 0x40;
    iVar5 = (*pcVar3)(&local_608,&local_648,&local_690,0,0);
    bVar4 = false;
    if ((iVar5 == 0) && (2 < local_690)) {
      bVar4 = ((char)local_648 == 'M' && local_648._1_1_ == 'a') && local_648._2_1_ == 'c';
      if ((((char)local_648 != 'M' || local_648._1_1_ != 'a') || local_648._2_1_ != 'c') &&
         (3 < local_690)) {
        bVar4 = (((char)local_648 == 'i' && local_648._1_1_ == 'M') && local_648._2_1_ == 'a') &&
                local_648._3_1_ == 'c';
      }
    }
    local_608 = (code *)0x0;
    local_600 = 0;
    local_610 = 0;
    local_618 = 0;
    local_620 = 0;
    local_628 = 0;
    local_630 = 0;
    local_638 = 0;
    local_640 = 0;
    local_648 = 0;
    local_691 = 0;
    local_6a8[4] = 0x952321b7;
    local_6a8[3] = 0xc3649291;
    local_6a8[2] = 0x9204229d;
    local_6a8[1] = 0xdb8da19f;
    local_660 = 0x5f76682e6e72656b;
    local_658 = 0x76;
    local_657 = 0x6d;
    local_656 = 0x6d;
    local_655 = 0x5f;
    local_654 = 0x70;
    local_653 = 0x72;
    local_652 = 0x65;
    local_651 = 0x73;
    local_650 = 0x65;
    local_64f = 0x6e;
    local_64e = 0x74;
    local_64d = 0;
    local_6a8[0] = 0;
    local_6b0 = 4;
    iVar5 = (*pcVar3)(&local_660,local_6a8,&local_6b0,0,0);
    uVar6 = 0;
    local_660 = 0;
    local_658 = 0;
    local_657 = 0;
    local_656 = 0;
    local_655 = 0;
    local_654 = 0;
    local_653 = 0;
    local_652 = 0;
    local_651 = 0;
    local_650 = 0;
    local_64f = 0;
    local_64e = 0;
    local_64d = 0;
    if (!(bool)((iVar5 != 0 || local_6a8[0] != 1) | bVar4)) {
      local_670 = 0x4d;
      local_66f = 0x61;
      local_66e = 99;
      local_66d = 0x68;
      local_66c = 0x69;
      local_66b = 0x6e;
      local_66a = 0x65;
      local_669 = 10;
      local_668 = 0;
      cVar9 = 'V';
      uVar6 = 0;
      do {
        uVar11 = uVar6;
        local_5f8[uVar11 + 0x148] = cVar9;
        cVar9 = *(char *)((long)&local_678 + uVar11 + 1);
        uVar6 = uVar11 + 1;
        if (cVar9 == '\0') break;
      } while (uVar6 < 0x3f);
      local_5f8[uVar11 + 0x149] = '\0';
      local_678 = 0;
      local_670 = 0;
      local_66f = 0;
      local_66e = 0;
      local_66d = 0;
      local_66c = 0;
      local_66b = 0;
      local_66a = 0;
      local_669 = 0;
      local_668 = 0;
    }
    if (((char *)0x3ff < pcVar14) ||
       (pcVar14[(long)(local_5f8 + 0x188)] = '\0', pcVar14 != (char *)0x0)) {
      uVar11 = (ulong)pcVar14 & 7;
      if (pcVar14 + -1 < (char *)0x7) {
        lVar15 = 0;
      }
      else {
        lVar15 = 0;
        pbVar7 = (byte *)(local_5f8 + 0x18b);
        do {
          bVar2 = pbVar7[-3] + 0x20;
          local_648 = CONCAT71(local_648._1_7_,bVar2);
          if (pbVar7[-3] - 0x41 < 0x1a) {
            pbVar7[-3] = bVar2;
          }
          bVar2 = pbVar7[-2] + 0x20;
          local_648 = CONCAT71(local_648._1_7_,bVar2);
          if (pbVar7[-2] - 0x41 < 0x1a) {
            pbVar7[-2] = bVar2;
          }
          bVar2 = pbVar7[-1] + 0x20;
          local_648 = CONCAT71(local_648._1_7_,bVar2);
          if (pbVar7[-1] - 0x41 < 0x1a) {
            pbVar7[-1] = bVar2;
          }
          bVar2 = *pbVar7 + 0x20;
          local_648 = CONCAT71(local_648._1_7_,bVar2);
          if (*pbVar7 - 0x41 < 0x1a) {
            *pbVar7 = bVar2;
          }
          bVar2 = pbVar7[1] + 0x20;
          local_648 = CONCAT71(local_648._1_7_,bVar2);
          if (pbVar7[1] - 0x41 < 0x1a) {
            pbVar7[1] = bVar2;
          }
          bVar2 = pbVar7[2] + 0x20;
          local_648 = CONCAT71(local_648._1_7_,bVar2);
          if (pbVar7[2] - 0x41 < 0x1a) {
            pbVar7[2] = bVar2;
          }
          bVar2 = pbVar7[3] + 0x20;
          local_648 = CONCAT71(local_648._1_7_,bVar2);
          if (pbVar7[3] - 0x41 < 0x1a) {
            pbVar7[3] = bVar2;
          }
          bVar2 = pbVar7[4] + 0x20;
          local_648 = CONCAT71(local_648._1_7_,bVar2);
          if (pbVar7[4] - 0x41 < 0x1a) {
            pbVar7[4] = bVar2;
          }
          lVar15 = lVar15 + -8;
          pbVar7 = pbVar7 + 8;
        } while (-lVar15 != ((ulong)pcVar14 & 0xfffffffffffffff8));
        lVar15 = -lVar15;
      }
      if (uVar11 != 0) {
        pbVar7 = (byte *)(local_5f8 + lVar15 + 0x188);
        do {
          bVar2 = *pbVar7 + 0x20;
          local_648 = CONCAT71(local_648._1_7_,bVar2);
          if (*pbVar7 - 0x41 < 0x1a) {
            *pbVar7 = bVar2;
          }
          pbVar7 = pbVar7 + 1;
          uVar11 = uVar11 - 1;
        } while (uVar11 != 0);
      }
    }
    if (uVar6 != 0) {
      uVar11 = uVar6 & 7;
      if (uVar6 < 8) {
        lVar15 = 0;
      }
      else {
        lVar15 = 0;
        pbVar7 = (byte *)(local_5f8 + 0x14b);
        do {
          if (pbVar7[-3] - 0x41 < 0x1a) {
            pbVar7[-3] = pbVar7[-3] | 0x20;
          }
          if (pbVar7[-2] - 0x41 < 0x1a) {
            pbVar7[-2] = pbVar7[-2] | 0x20;
          }
          if (pbVar7[-1] - 0x41 < 0x1a) {
            pbVar7[-1] = pbVar7[-1] | 0x20;
          }
          if (*pbVar7 - 0x41 < 0x1a) {
            *pbVar7 = *pbVar7 | 0x20;
          }
          if (pbVar7[1] - 0x41 < 0x1a) {
            pbVar7[1] = pbVar7[1] | 0x20;
          }
          if (pbVar7[2] - 0x41 < 0x1a) {
            pbVar7[2] = pbVar7[2] | 0x20;
          }
          if (pbVar7[3] - 0x41 < 0x1a) {
            pbVar7[3] = pbVar7[3] | 0x20;
          }
          if (pbVar7[4] - 0x41 < 0x1a) {
            pbVar7[4] = pbVar7[4] | 0x20;
          }
          lVar15 = lVar15 + -8;
          pbVar7 = pbVar7 + 8;
        } while (-lVar15 != (uVar6 & 0xfffffffffffffff8));
        lVar15 = -lVar15;
      }
      if (uVar11 != 0) {
        pbVar7 = (byte *)(local_5f8 + lVar15 + 0x148);
        do {
          if (*pbVar7 - 0x41 < 0x1a) {
            *pbVar7 = *pbVar7 | 0x20;
          }
          pbVar7 = pbVar7 + 1;
          uVar11 = uVar11 - 1;
        } while (uVar11 != 0);
      }
    }
    if ((char *)0x23 < pcVar14) {
      lVar15 = 0;
      pcVar8 = local_5f8 + 0x188;
LAB_100091d48:
      lVar17 = 0;
      iVar5 = 0x1505;
      do {
        iVar5 = iVar5 * 0x21 + (uint)(byte)pcVar8[lVar17];
        lVar17 = lVar17 + 1;
      } while (lVar17 != 0x24);
      if (iVar5 != 0x676d1aa2) goto code_r0x000100091d70;
      lVar15 = 0;
      do {
        local_5f8[lVar15 + 0x188] = '\0';
        lVar15 = lVar15 + 1;
      } while (lVar15 != 0x400);
      uVar12 = 0;
      goto LAB_100091fcc;
    }
LAB_100091d84:
    uVar12 = 0;
    puVar13 = &DAT_10009f20f;
    lVar15 = 1;
    do {
      FUN_10009de8c(puVar13,(&UNK_10009f377)[lVar15],0x9d,&local_648);
      lVar17 = FUN_10009dfc0(local_5f8 + 0x148,&local_648);
      if (lVar17 == 0) {
        lVar17 = FUN_10009dfc0(local_5f8 + 0x188,&local_648);
        bVar4 = lVar17 == 0;
      }
      else {
        bVar4 = false;
      }
      local_648 = 0;
      local_640 = 0;
      local_638 = 0;
      local_630 = 0;
      if (!bVar4) {
        uVar12 = 0x13b6dfe;
      }
      lVar15 = lVar15 + 1;
      puVar13 = puVar13 + 0x24;
      local_628 = 0;
    } while (lVar15 != 4);
    puVar13 = &DAT_10009f27b;
    lVar15 = 4;
    do {
      local_628 = 0;
      local_630 = 0;
      local_638 = 0;
      local_640 = 0;
      local_648 = 0;
      FUN_10009de8c(puVar13,(&UNK_10009f377)[lVar15],0x9d,&local_648);
      lVar17 = FUN_10009dfc0(local_5f8 + 0x188,&local_648);
      local_648 = 0;
      local_640 = 0;
      local_638 = 0;
      local_630 = 0;
      uVar1 = 0;
      if (lVar17 != 0) {
        uVar1 = 1 << (ulong)((uint)lVar15 & 0x1f) | 0x13b6dfe;
      }
      uVar12 = uVar1 | uVar12;
      lVar15 = lVar15 + 1;
      puVar13 = puVar13 + 0x24;
      local_628 = 0;
    } while (lVar15 != 0xb);
    lVar15 = 0;
    do {
      local_5f8[lVar15 + 0x188] = '\0';
      lVar15 = lVar15 + 1;
    } while (lVar15 != 0x400);
LAB_100091fcc:
    local_5f8[0x148] = 0;
    local_5f8[0x149] = 0;
    local_5f8[0x14a] = 0;
    local_5f8[0x14b] = 0;
    local_5f8[0x14c] = 0;
    local_5f8[0x14d] = 0;
    local_5f8[0x14e] = 0;
    local_5f8[0x14f] = 0;
    local_5f8[0x150] = 0;
    local_5f8[0x151] = 0;
    local_5f8[0x152] = 0;
    local_5f8[0x153] = 0;
    local_5f8[0x154] = 0;
    local_5f8[0x155] = 0;
    local_5f8[0x156] = 0;
    local_5f8[0x157] = 0;
    local_5f8[0x158] = 0;
    local_5f8[0x159] = 0;
    local_5f8[0x15a] = 0;
    local_5f8[0x15b] = 0;
    local_5f8[0x15c] = 0;
    local_5f8[0x15d] = 0;
    local_5f8[0x15e] = 0;
    local_5f8[0x15f] = 0;
    local_5f8[0x160] = 0;
    local_5f8[0x161] = 0;
    local_5f8[0x162] = 0;
    local_5f8[0x163] = 0;
    local_5f8[0x164] = 0;
    local_5f8[0x165] = 0;
    local_5f8[0x166] = 0;
    local_5f8[0x167] = 0;
    local_5f8[0x168] = 0;
    local_5f8[0x169] = 0;
    local_5f8[0x16a] = 0;
    local_5f8[0x16b] = 0;
    local_5f8[0x16c] = 0;
    local_5f8[0x16d] = 0;
    local_5f8[0x16e] = 0;
    local_5f8[0x16f] = 0;
    local_5f8[0x170] = 0;
    local_5f8[0x171] = 0;
    local_5f8[0x172] = 0;
    local_5f8[0x173] = 0;
    local_5f8[0x174] = 0;
    local_5f8[0x175] = 0;
    local_5f8[0x176] = 0;
    local_5f8[0x177] = 0;
    local_5f8[0x178] = 0;
    local_5f8[0x179] = 0;
    local_5f8[0x17a] = 0;
    local_5f8[0x17b] = 0;
    local_5f8[0x17c] = 0;
    local_5f8[0x17d] = 0;
    local_5f8[0x17e] = 0;
    local_5f8[0x17f] = 0;
    local_5f8[0x180] = 0;
    local_5f8[0x181] = 0;
    local_5f8[0x182] = 0;
    local_5f8[0x183] = 0;
    local_5f8[0x184] = 0;
    local_5f8[0x185] = 0;
    local_5f8[0x186] = 0;
    local_5f8[0x187] = 0;
  }
  if (*(long *)PTR____stack_chk_guard_100102830 == local_70) {
    return uVar12;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
code_r0x000100091d70:
  pcVar16 = (char *)(lVar15 + 0x25);
  lVar15 = lVar15 + 1;
  pcVar8 = pcVar8 + 1;
  if (pcVar14 < pcVar16) goto LAB_100091d84;
  goto LAB_100091d48;
}

