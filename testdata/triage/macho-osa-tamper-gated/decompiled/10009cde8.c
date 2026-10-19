// FUN_10009cde8 @ 10009cde8

void FUN_10009cde8(byte *param_1,long param_2,uint *param_3)

{
  byte *pbVar1;
  ulong uVar2;
  ulong uVar3;
  uint uVar4;
  uint uVar5;
  byte *pbVar6;
  uint local_ec;
  uint local_e8;
  byte local_e1;
  undefined8 local_e0;
  undefined8 local_d8;
  undefined8 local_d0;
  undefined8 local_c8;
  long local_c0;
  byte local_b8 [64];
  ulong local_78;
  long local_70;
  byte *pbVar7;
  
  local_70 = *(long *)PTR____stack_chk_guard_100102830;
  local_e8 = 0x6f3c2891;
  local_ec = 0xec913fb;
  do {
    if ((int)local_e8 < -0x1899f2ee) {
      if ((int)local_e8 < -0x34d173cf) {
        if (local_e8 == 0x88e7228f) {
          FUN_10009d22c(&local_e0);
          uVar4 = ((uint)local_e0 & 0xff00ff00) >> 8 | ((uint)local_e0 & 0xff00ff) << 8;
          uVar5 = (local_e0._4_4_ & 0xff00ff00) >> 8 | (local_e0._4_4_ & 0xff00ff) << 8;
          *param_3 = uVar4 >> 0x10 | uVar4 << 0x10;
          param_3[1] = uVar5 >> 0x10 | uVar5 << 0x10;
          uVar4 = ((uint)local_d8 & 0xff00ff00) >> 8 | ((uint)local_d8 & 0xff00ff) << 8;
          uVar5 = (local_d8._4_4_ & 0xff00ff00) >> 8 | (local_d8._4_4_ & 0xff00ff) << 8;
          param_3[2] = uVar4 >> 0x10 | uVar4 << 0x10;
          param_3[3] = uVar5 >> 0x10 | uVar5 << 0x10;
          uVar4 = ((uint)local_d0 & 0xff00ff00) >> 8 | ((uint)local_d0 & 0xff00ff) << 8;
          uVar5 = (local_d0._4_4_ & 0xff00ff00) >> 8 | (local_d0._4_4_ & 0xff00ff) << 8;
          param_3[4] = uVar4 >> 0x10 | uVar4 << 0x10;
          param_3[5] = uVar5 >> 0x10 | uVar5 << 0x10;
          uVar4 = ((uint)local_c8 & 0xff00ff00) >> 8 | ((uint)local_c8 & 0xff00ff) << 8;
          uVar5 = (local_c8._4_4_ & 0xff00ff00) >> 8 | (local_c8._4_4_ & 0xff00ff) << 8;
          param_3[6] = uVar4 >> 0x10 | uVar4 << 0x10;
          param_3[7] = uVar5 >> 0x10 | uVar5 << 0x10;
          local_e8 = 0xd31c622e;
        }
        else {
          if (local_e8 != 0x999cb14d) goto LAB_10009d1f0;
          pbVar7 = local_b8 + local_78;
          local_78 = local_78 + 1;
          *pbVar7 = 0x80;
          uVar3 = local_78;
          local_e8 = 0xcbc88157;
          if (0x38 < local_78) {
            if (local_78 < 0x40) {
              uVar2 = local_78 + 1;
              pbVar7 = local_b8 + local_78;
              local_78 = uVar2;
              *pbVar7 = 0;
              if (uVar2 != 0x40) {
                local_78 = uVar3 + 2;
                local_b8[uVar3 + 1] = 0;
                if (uVar3 + 2 != 0x40) {
                  local_78 = uVar3 + 3;
                  local_b8[uVar3 + 2] = 0;
                  if (uVar3 + 3 != 0x40) {
                    local_78 = uVar3 + 4;
                    local_b8[uVar3 + 3] = 0;
                    if (uVar3 + 4 != 0x40) {
                      local_78 = uVar3 + 5;
                      local_b8[uVar3 + 4] = 0;
                      if (uVar3 + 5 != 0x40) {
                        local_78 = uVar3 + 6;
                        local_b8[uVar3 + 5] = 0;
                        if (uVar3 + 6 != 0x40) {
                          local_78 = uVar3 + 7;
                          local_b8[uVar3 + 6] = 0;
                        }
                      }
                    }
                  }
                }
              }
            }
            FUN_10009d22c(&local_e0);
            local_78 = 0;
            local_e8 = 0xcbc88157;
          }
        }
      }
      else if (local_e8 == 0xcb2e8c31) {
        local_e0 = DAT_1001060c8;
        local_d8 = DAT_1001060d0;
        local_d0 = DAT_1001060d8;
        local_c8 = DAT_1001060e0;
        local_c0 = 0;
        local_e8 = 0xe685c9de;
      }
      else {
        if (local_e8 != 0xdfa1443b) goto LAB_10009d1f0;
        local_78 = 0;
        local_e1 = 0;
        local_e8 = 0xa0f35a45;
      }
    }
    else if ((int)local_e8 < 0x4923fe65) {
      if (local_e8 == 0xe7660d12) {
        local_e8 = 0xed99a5b4;
      }
      else {
        if (local_e8 != 0x2fc33c45) {
LAB_10009d1f0:
          if (*(long *)PTR____stack_chk_guard_100102830 != local_70) {
                    /* WARNING: Subroutine does not return */
            ___stack_chk_fail();
          }
          return;
        }
        pbVar7 = param_1;
        if (param_2 != 0) {
          do {
            pbVar6 = pbVar7 + 1;
            pbVar1 = local_b8 + local_78;
            local_78 = local_78 + 1;
            *pbVar1 = local_e1 ^ *pbVar7;
            if (local_78 == 0x40) {
              FUN_10009d22c(&local_e0);
              local_c0 = local_c0 + 0x200;
              local_78 = 0;
            }
            pbVar7 = pbVar6;
          } while (pbVar6 < param_1 + param_2);
        }
        local_c0 = local_c0 + local_78 * 8;
        local_e8 = 0x59149012;
      }
    }
    else if (local_e8 == 0x4923fe65) {
      if (local_78 < 0x38) {
        do {
          uVar3 = local_78 + 1;
          local_b8[local_78] = 0;
          local_78 = uVar3;
        } while (uVar3 != 0x38);
        local_78 = 0x38;
      }
      pbVar7 = local_b8 + local_78;
      local_78 = local_78 + 1;
      *pbVar7 = (byte)((ulong)local_c0 >> 0x38);
      pbVar7 = local_b8 + local_78;
      local_78 = local_78 + 1;
      *pbVar7 = (byte)((ulong)local_c0 >> 0x30);
      pbVar7 = local_b8 + local_78;
      local_78 = local_78 + 1;
      *pbVar7 = (byte)((ulong)local_c0 >> 0x28);
      pbVar7 = local_b8 + local_78;
      local_78 = local_78 + 1;
      *pbVar7 = (byte)((ulong)local_c0 >> 0x20);
      pbVar7 = local_b8 + local_78;
      local_78 = local_78 + 1;
      *pbVar7 = (byte)((ulong)local_c0 >> 0x18);
      pbVar7 = local_b8 + local_78;
      local_78 = local_78 + 1;
      *pbVar7 = (byte)((ulong)local_c0 >> 0x10);
      pbVar7 = local_b8 + local_78;
      local_78 = local_78 + 1;
      *pbVar7 = (byte)((ulong)local_c0 >> 8);
      pbVar7 = local_b8 + local_78;
      local_78 = local_78 + 1;
      *pbVar7 = (byte)local_c0;
      local_e8 = 0xaa137666;
    }
    else {
      if (local_e8 != 0x6f3c2891) goto LAB_10009d1f0;
      FUN_10009d668();
      local_e8 = 0xc533752f;
    }
    local_ec = local_ec * 0x19660d + 0x3c6ef35f;
    local_e8 = local_ec ^ local_e8;
  } while( true );
}

