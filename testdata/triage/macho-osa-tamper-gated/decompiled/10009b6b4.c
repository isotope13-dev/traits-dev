// FUN_10009b6b4 @ 10009b6b4

void FUN_10009b6b4(undefined8 param_1)

{
  kern_return_t kVar1;
  int iVar2;
  long lVar3;
  ulong uVar4;
  long lVar5;
  long unaff_x25;
  int *unaff_x26;
  undefined8 local_c0;
  uint local_b4;
  uint local_b0;
  mach_msg_type_number_t local_ac;
  int *local_a8;
  undefined8 uStack_a0;
  undefined8 local_98;
  undefined8 uStack_90;
  undefined8 local_88;
  undefined8 uStack_80;
  undefined8 local_78;
  undefined8 uStack_70;
  long local_68;
  
  uVar4 = 0;
  local_68 = *(long *)PTR____stack_chk_guard_100102830;
  local_b0 = 0xcda458f5;
  local_b4 = 0x96222f06;
  do {
    lVar3 = 0;
    if ((int)local_b0 < 0x15cd553d) {
      if ((int)local_b0 < -0x141fc13d) {
        if (local_b0 == 0x967fbbe0) {
          if (unaff_x26 == (int *)0x0) {
            lVar3 = 0;
            goto LAB_10009b958;
          }
          if (*unaff_x26 == 0) {
            lVar3 = 0;
            goto LAB_10009b958;
          }
          local_b0 = 0xe9570aa7;
        }
        else {
          if (local_b0 != 0xcda458f5) goto LAB_10009b958;
          local_78 = 0;
          uStack_70 = 0;
          local_88 = 0;
          uStack_80 = 0;
          local_98 = 0;
          uStack_90 = 0;
          local_b0 = 0xf99d846e;
          local_a8 = (int *)0x0;
          uStack_a0 = 0;
        }
      }
      else if (local_b0 == 0xebe03ec3) {
        local_ac = 0x10;
        local_b0 = 0xfe1d1fd9;
      }
      else {
        if (local_b0 != 0xec0759ca) goto LAB_10009b958;
        unaff_x25 = *(long *)(unaff_x26 + 2);
        local_b0 = 0x26fe0e92;
      }
    }
    else if ((int)local_b0 < 0x5c8c44d9) {
      if (local_b0 == 0x15cd553d) {
        uVar4 = (ulong)(uint)unaff_x26[1];
        if (uVar4 - 0x4001 < 0xffffffffffffc000) {
          lVar3 = 0;
          goto LAB_10009b958;
        }
        local_b0 = 0x46073fb;
      }
      else {
        if (local_b0 != 0x243f44cf) goto LAB_10009b958;
        local_b0 = 0x7e591ff7;
      }
    }
    else if (local_b0 == 0x5c8c44d9) {
      local_b0 = 0x1ea5c83e;
    }
    else if (local_b0 == 0x65ba934e) {
      if (unaff_x25 == 0) {
        lVar3 = 0;
        goto LAB_10009b958;
      }
      if (uVar4 == 0) {
        local_b0 = 0x4757e61;
      }
      else {
        lVar5 = 0;
        do {
          lVar3 = *(long *)(unaff_x25 + lVar5);
          if (lVar3 != 0) {
            local_c0 = 0;
            iVar2 = FUN_10009ba50(lVar3,&local_c0);
            if ((iVar2 != 0) && (lVar3 = FUN_10009bc14(lVar3,local_c0,param_1), lVar3 != 0))
            goto LAB_10009b958;
          }
          lVar5 = lVar5 + 0x18;
        } while (uVar4 * 0x18 - lVar5 != 0);
        local_b0 = 0x4757e61;
      }
    }
    else {
      if (local_b0 != 0x7e0a43f1) goto LAB_10009b958;
      kVar1 = _task_info(*(task_name_t *)PTR__mach_task_self__100102838,0x11,(task_info_t)&local_a8,
                         &local_ac);
      if (kVar1 != 0) {
        lVar3 = 0;
LAB_10009b958:
        if (*(long *)PTR____stack_chk_guard_100102830 != local_68) {
                    /* WARNING: Subroutine does not return */
          ___stack_chk_fail(lVar3);
        }
        return;
      }
      local_b0 = 0x9a412a87;
      unaff_x26 = local_a8;
    }
    local_b4 = local_b4 * 0x19660d + 0x3c6ef35f;
    local_b0 = local_b4 ^ local_b0;
  } while( true );
}

