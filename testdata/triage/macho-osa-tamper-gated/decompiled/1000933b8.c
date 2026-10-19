// FUN_1000933b8 @ 1000933b8

void FUN_1000933b8(undefined8 param_1,undefined1 *param_2,undefined8 *param_3)

{
  code *pcVar1;
  long lVar2;
  int iVar3;
  undefined1 *unaff_x22;
  uint local_d0;
  uint local_cc;
  undefined8 local_c8;
  undefined8 uStack_c0;
  undefined8 local_b8;
  undefined8 uStack_b0;
  undefined8 local_a8;
  undefined8 uStack_a0;
  undefined8 local_98;
  undefined8 uStack_90;
  undefined8 local_88;
  undefined8 uStack_80;
  undefined8 local_78;
  undefined8 uStack_70;
  long local_68;
  
  local_68 = *(long *)PTR____stack_chk_guard_100102830;
  local_cc = 0x35cad679;
  local_d0 = 0x3fa2cd3e;
  do {
    if ((int)local_cc < -0x33120ea6) {
      if ((int)local_cc < -0x50a1fdc5) {
        if (local_cc == 0x8a62097f) {
          local_cc = 0x8ff61e7a;
        }
        else {
          if (local_cc != 0x9ada9b43) goto LAB_1000937b8;
          *unaff_x22 = 0;
          unaff_x22[1] = 0;
          unaff_x22[2] = 0;
          unaff_x22[3] = 0;
          unaff_x22[4] = 0;
          unaff_x22[5] = 0;
          unaff_x22[6] = 0;
          unaff_x22[7] = 0;
          unaff_x22[8] = 0;
          unaff_x22[9] = 0;
          unaff_x22[10] = 0;
          unaff_x22[0xb] = 0;
          unaff_x22[0xc] = 0;
          unaff_x22[0xd] = 0;
          unaff_x22[0xe] = 0;
          unaff_x22[0xf] = 0;
          unaff_x22[0x10] = 0;
          unaff_x22[0x11] = 0;
          unaff_x22[0x12] = 0;
          unaff_x22[0x13] = 0;
          unaff_x22[0x14] = 0;
          unaff_x22[0x15] = 0;
          unaff_x22[0x16] = 0;
          unaff_x22[0x17] = 0;
          unaff_x22[0x18] = 0;
          unaff_x22[0x19] = 0;
          unaff_x22[0x1a] = 0;
          unaff_x22[0x1b] = 0;
          unaff_x22[0x1c] = 0;
          unaff_x22[0x1d] = 0;
          unaff_x22[0x1e] = 0;
          unaff_x22[0x1f] = 0;
          unaff_x22[0x20] = 0;
          unaff_x22[0x21] = 0;
          unaff_x22[0x22] = 0;
          local_cc = 0x4324c38a;
          unaff_x22[0x23] = 0;
        }
      }
      else if (local_cc == 0xaf5e023b) {
        if (unaff_x22 == (undefined1 *)0x0) {
                    /* WARNING: Does not return */
          pcVar1 = (code *)SoftwareBreakpoint(1,0x1000937f4);
          (*pcVar1)();
        }
        local_cc = 0xfcbb556c;
      }
      else {
        if (local_cc != 0xc2050029) goto LAB_1000937b8;
        _free(unaff_x22);
        local_cc = 0x407c33d2;
      }
    }
    else if ((int)local_cc < 0x310bd03e) {
      if (local_cc == 0xccedf15a) {
        unaff_x22 = _malloc(0x24);
        local_cc = 0x8f1ed5c4;
      }
      else {
        if (local_cc != 0xf701d2da) {
LAB_1000937b8:
          if (*(long *)PTR____stack_chk_guard_100102830 == local_68) {
            return;
          }
                    /* WARNING: Subroutine does not return */
          ___stack_chk_fail();
        }
        *(undefined4 *)(unaff_x22 + 0x20) = 0x1000000;
        FUN_10009d864(param_1,0x24,unaff_x22,0x24,&local_88);
        local_a8 = local_88;
        uStack_a0 = uStack_80;
        local_98 = local_78;
        uStack_90 = uStack_70;
        iVar3 = 1;
        do {
          FUN_10009d864(param_1,0x24,&local_a8,0x20,&local_c8);
          lVar2 = 0;
          local_a8 = local_c8;
          uStack_a0 = uStack_c0;
          local_98 = local_b8;
          uStack_90 = uStack_b0;
          do {
            *(byte *)((long)&local_88 + lVar2) =
                 *(byte *)((long)&local_88 + lVar2) ^ *(byte *)((long)&local_c8 + lVar2);
            lVar2 = lVar2 + 1;
          } while (lVar2 != 0x20);
          iVar3 = iVar3 + 1;
        } while (iVar3 != 0x1757e);
        *param_3 = local_88;
        param_3[1] = uStack_80;
        param_3[2] = local_78;
        param_3[3] = uStack_70;
        local_cc = 0x926b3f17;
      }
    }
    else if (local_cc == 0x44fa8daf) {
      local_cc = 0xf02cc053;
    }
    else if (local_cc == 0x35cad679) {
      local_cc = 0xeaea1afa;
    }
    else {
      if (local_cc != 0x310bd03e) goto LAB_1000937b8;
      *unaff_x22 = *param_2;
      unaff_x22[1] = param_2[1];
      unaff_x22[2] = param_2[2];
      unaff_x22[3] = param_2[3];
      unaff_x22[4] = param_2[4];
      unaff_x22[5] = param_2[5];
      unaff_x22[6] = param_2[6];
      unaff_x22[7] = param_2[7];
      unaff_x22[8] = param_2[8];
      unaff_x22[9] = param_2[9];
      unaff_x22[10] = param_2[10];
      unaff_x22[0xb] = param_2[0xb];
      unaff_x22[0xc] = param_2[0xc];
      unaff_x22[0xd] = param_2[0xd];
      unaff_x22[0xe] = param_2[0xe];
      unaff_x22[0xf] = param_2[0xf];
      unaff_x22[0x10] = param_2[0x10];
      unaff_x22[0x11] = param_2[0x11];
      unaff_x22[0x12] = param_2[0x12];
      unaff_x22[0x13] = param_2[0x13];
      unaff_x22[0x14] = param_2[0x14];
      unaff_x22[0x15] = param_2[0x15];
      unaff_x22[0x16] = param_2[0x16];
      unaff_x22[0x17] = param_2[0x17];
      unaff_x22[0x18] = param_2[0x18];
      unaff_x22[0x19] = param_2[0x19];
      unaff_x22[0x1a] = param_2[0x1a];
      unaff_x22[0x1b] = param_2[0x1b];
      unaff_x22[0x1c] = param_2[0x1c];
      unaff_x22[0x1d] = param_2[0x1d];
      unaff_x22[0x1e] = param_2[0x1e];
      unaff_x22[0x1f] = param_2[0x1f];
      local_cc = 0xff87b653;
    }
    local_d0 = local_d0 * 0x19660d + 0x3c6ef35f;
    local_cc = local_d0 ^ local_cc;
  } while( true );
}

