// FUN_10009d22c @ 10009d22c

void FUN_10009d22c(uint *param_1)

{
  int iVar1;
  ulong uVar2;
  uint uVar3;
  uint uVar4;
  uint uVar5;
  uint uVar6;
  uint uVar7;
  uint uVar8;
  uint uVar9;
  long lVar10;
  long lVar11;
  uint in_w13;
  ulong in_x15;
  int *piVar12;
  ulong uVar13;
  uint unaff_w20;
  ulong unaff_x21;
  ulong unaff_x22;
  uint *puVar14;
  ulong unaff_x25;
  ulong uVar15;
  uint unaff_w27;
  uint local_17c;
  uint local_178;
  uint local_174;
  uint local_170 [16];
  int aiStack_130 [48];
  long local_70;
  
  local_70 = *(long *)PTR____stack_chk_guard_100102830;
  local_174 = 0x685cbcbc;
  local_178 = 0x588731a5;
  do {
    if ((int)local_174 < 0x49092e4) {
      if ((int)local_174 < -0x2e8cf517) {
        if (local_174 == 0xa8917beb) {
          *param_1 = *param_1 + (int)unaff_x22;
          param_1[1] = param_1[1] + (int)in_x15;
          local_174 = 0x15c5c64d;
        }
        else {
          if (local_174 != 0xd1238dfa) goto LAB_10009d62c;
          local_174 = 0x2e591c49;
        }
      }
      else if (local_174 == 0xd1730ae9) {
        param_1[4] = param_1[4] + unaff_w27;
        param_1[5] = param_1[5] + in_w13;
        local_174 = 0xe898bde7;
      }
      else {
        if (local_174 != 0xff917524) goto LAB_10009d62c;
        param_1[6] = param_1[6] + unaff_w20;
        param_1[7] = param_1[7] + local_17c;
        local_174 = 0x62092c72;
      }
    }
    else if ((int)local_174 < 0x3ad1a6a8) {
      if (local_174 == 0x49092e4) {
        param_1[2] = param_1[2] + (int)unaff_x21;
        param_1[3] = param_1[3] + (int)unaff_x25;
        local_174 = 0xb3739f1d;
      }
      else {
        if (local_174 != 0x2c25db8e) {
LAB_10009d62c:
          if (*(long *)PTR____stack_chk_guard_100102830 == local_70) {
            return;
          }
                    /* WARNING: Subroutine does not return */
          ___stack_chk_fail();
        }
        lVar10 = 0x30;
        piVar12 = aiStack_130;
        uVar6 = local_170[0];
        do {
          uVar7 = piVar12[-0xf];
          uVar8 = FUN_10009d6d4(uVar7,7);
          uVar3 = FUN_10009d6d4(uVar7,0x12);
          uVar9 = piVar12[-2];
          uVar4 = FUN_10009d6d4(uVar9,0x11);
          uVar5 = FUN_10009d6d4(uVar9,0x13);
          *piVar12 = uVar6 + piVar12[-7] + (uVar8 ^ uVar7 >> 3 ^ uVar3) +
                     (uVar4 ^ uVar9 >> 10 ^ uVar5);
          lVar10 = lVar10 + -1;
          piVar12 = piVar12 + 1;
          uVar6 = uVar7;
        } while (lVar10 != 0);
        unaff_x22 = (ulong)*param_1;
        in_x15 = (ulong)param_1[1];
        local_174 = 0xb21ff463;
        unaff_x21 = (ulong)param_1[2];
        unaff_x25 = (ulong)param_1[3];
      }
    }
    else if (local_174 == 0x3ad1a6a8) {
      local_174 = 0xfc1e47d7;
    }
    else if (local_174 == 0x4f60cf7c) {
      uVar13 = 0x29;
      uVar2 = in_x15;
      puVar14 = local_170;
      uVar15 = unaff_x25;
      uVar6 = param_1[5];
      uVar7 = param_1[6];
      uVar9 = param_1[7];
      unaff_w27 = param_1[4];
      do {
        in_w13 = unaff_w27;
        local_17c = uVar7;
        unaff_w20 = uVar6;
        in_x15 = unaff_x22;
        unaff_x25 = unaff_x21;
        unaff_x21 = uVar2;
        uVar6 = FUN_10009d6d4(in_w13,6);
        uVar7 = FUN_10009d6d4(in_w13,0xb);
        uVar8 = FUN_10009d6d4(in_w13,0x19);
        iVar1 = (in_w13 & unaff_w20 | local_17c & (in_w13 ^ 0xffffffff)) + uVar9 +
                (uVar7 ^ uVar6 ^ uVar8) + *puVar14 + (&DAT_1001060e8)[uVar13 & 0x3f];
        uVar6 = FUN_10009d6d4(in_x15,2);
        uVar7 = FUN_10009d6d4(in_x15,0xd);
        uVar9 = FUN_10009d6d4(in_x15,0x16);
        unaff_w27 = iVar1 + (int)uVar15;
        unaff_x22 = (ulong)(iVar1 + ((uint)in_x15 & ((uint)unaff_x21 ^ (uint)unaff_x25) ^
                                    (uint)unaff_x21 & (uint)unaff_x25) + (uVar7 ^ uVar6 ^ uVar9));
        uVar13 = uVar13 + 1;
        uVar2 = in_x15;
        puVar14 = puVar14 + 1;
        uVar15 = unaff_x25;
        uVar6 = in_w13;
        uVar7 = unaff_w20;
        uVar9 = local_17c;
      } while (uVar13 != 0x69);
      local_174 = 0x3beb3619;
    }
    else {
      if (local_174 != 0x685cbcbc) goto LAB_10009d62c;
      FUN_10009d6a4();
      lVar10 = 0;
      lVar11 = (long)param_1 + 0x2b;
      do {
        uVar6 = (*(uint *)(lVar11 + -3) & 0xff00ff00) >> 8 |
                (*(uint *)(lVar11 + -3) & 0xff00ff) << 8;
        local_170[lVar10] = uVar6 >> 0x10 | uVar6 << 0x10;
        lVar10 = lVar10 + 1;
        lVar11 = lVar11 + 4;
      } while (lVar10 != 0x10);
      local_174 = 0x5e14ed4e;
    }
    local_178 = local_178 * 0x19660d + 0x3c6ef35f;
    local_174 = local_178 ^ local_174;
  } while( true );
}

