// FUN_10008f4b0 @ 10008f4b0

uint FUN_10008f4b0(void)

{
  ulong uVar1;
  char cVar2;
  byte *pbVar3;
  code *pcVar4;
  code *pcVar5;
  bool bVar6;
  bool bVar7;
  uint uVar8;
  undefined4 uVar9;
  int iVar10;
  char *pcVar11;
  long lVar12;
  long lVar13;
  ulong uVar14;
  ulong uVar15;
  byte bVar16;
  char cVar17;
  uint uVar18;
  ulong uVar19;
  int *piVar20;
  ulong uVar21;
  uint uVar22;
  ulong uVar23;
  uint *puVar24;
  undefined *puVar25;
  undefined1 *puVar26;
  long lVar27;
  uint uVar28;
  code *local_4728;
  undefined8 local_4720;
  uint local_4718;
  uint local_4714;
  int local_4710;
  int local_470c;
  int local_4708;
  int local_4704;
  int local_4700;
  int local_46fc;
  int local_46f8;
  uint local_46f4;
  uint local_46f0;
  char local_46ea;
  char local_46e9;
  char local_46e8;
  char local_46e7;
  char local_46e6;
  char local_46e5;
  char local_46e4;
  char local_46e3;
  char local_46e2;
  char local_46e1;
  char local_46e0;
  char local_46df;
  char local_46de;
  char local_46dd;
  char local_46dc;
  char local_46db;
  char local_46da;
  char local_46d9;
  char local_46d8;
  char local_46d7;
  char local_46d6;
  char local_46d5;
  char local_46d4;
  char local_46d3;
  char local_46d2;
  char local_46d1;
  code *local_46d0;
  undefined8 uStack_46c8;
  undefined8 local_46c0;
  undefined8 uStack_46b8;
  undefined8 local_46b0;
  undefined8 uStack_46a8;
  undefined8 local_46a0;
  undefined8 uStack_4698;
  undefined8 local_4690;
  undefined8 uStack_4688;
  undefined8 local_4680;
  undefined8 uStack_4678;
  undefined8 local_4670;
  undefined8 uStack_4668;
  undefined8 local_4660;
  undefined8 uStack_4658;
  undefined8 local_4650;
  undefined8 local_4648;
  long local_4640;
  undefined8 uStack_4638;
  undefined8 local_4630;
  undefined8 uStack_4628;
  undefined8 local_4620;
  undefined8 uStack_4618;
  undefined8 local_4610;
  undefined8 uStack_4608;
  undefined8 local_4600;
  undefined8 uStack_45f8;
  undefined8 local_45f0;
  undefined8 uStack_45e8;
  undefined8 local_45e0;
  undefined8 uStack_45d8;
  undefined8 local_3560;
  undefined8 local_3558;
  undefined8 local_3550;
  undefined8 local_3548;
  undefined8 local_3540;
  undefined8 local_3538;
  undefined8 local_3530;
  undefined8 local_3528;
  undefined8 local_3520;
  undefined8 local_3518;
  undefined8 local_3510;
  undefined8 local_3508;
  undefined8 local_3500;
  undefined8 local_34f8;
  undefined8 local_34f0;
  undefined8 local_34e8;
  undefined8 local_2560;
  long local_2558;
  long local_2550;
  long local_2548;
  undefined8 local_2540;
  undefined8 local_2538;
  undefined8 local_2530;
  undefined8 local_2528;
  undefined8 local_2520;
  undefined8 local_2518;
  undefined8 local_2510;
  undefined8 local_2508;
  undefined8 local_2500;
  undefined8 local_24f8;
  undefined8 local_24f0;
  undefined8 local_24e8;
  undefined8 local_24e0;
  undefined8 local_24d8;
  undefined8 local_24d0;
  undefined8 local_24c8;
  undefined8 local_24c0;
  undefined8 local_24b8;
  undefined8 local_24b0;
  undefined8 local_24a8;
  undefined8 local_24a0;
  undefined8 local_2498;
  undefined8 local_2490;
  undefined8 local_2488;
  undefined8 local_2480;
  undefined8 local_2478;
  undefined8 local_2470;
  undefined8 local_2468;
  char local_7d;
  char local_7c;
  char local_7b;
  char local_7a;
  char local_79;
  char local_78;
  char local_77;
  char local_76;
  char local_75;
  char local_74;
  char local_73;
  char local_72;
  char local_71;
  long local_70;
  
  local_70 = *(long *)PTR____stack_chk_guard_100102830;
  local_46d1 = DAT_10009e908;
  local_46d2 = DAT_10009e909;
  local_46d3 = DAT_10009e90a;
  local_46d4 = DAT_10009e90b;
  local_46d5 = DAT_10009e90c;
  local_46d6 = DAT_10009e90d;
  local_46d7 = DAT_10009e90e;
  local_46d8 = DAT_10009e90f;
  local_46d9 = DAT_10009e910;
  local_46da = DAT_10009e911;
  local_46db = DAT_10009e912;
  local_46dc = DAT_10009e913;
  local_46dd = DAT_10009e914;
  local_46de = DAT_10009e915;
  local_46df = DAT_10009e916;
  local_46e0 = DAT_10009e917;
  local_46e1 = DAT_10009e918;
  local_46e2 = DAT_10009e919;
  local_46e3 = DAT_10009e91a;
  local_46e4 = DAT_10009e91b;
  local_46e5 = DAT_10009e91c;
  local_46e6 = DAT_10009e91d;
  local_46e7 = DAT_10009e91e;
  local_46e8 = DAT_10009e91f;
  local_46e9 = DAT_10009e920;
  local_46ea = DAT_10009e921;
  local_7d = DAT_10009e915 + DAT_10009e908;
  local_7c = DAT_10009e916 + DAT_10009e909;
  local_7b = DAT_10009e917 + DAT_10009e90a;
  local_7a = DAT_10009e918 + DAT_10009e90b;
  local_79 = DAT_10009e919 + DAT_10009e90c;
  local_78 = DAT_10009e91a + DAT_10009e90d;
  local_77 = DAT_10009e91b + DAT_10009e90e;
  local_76 = DAT_10009e91c + DAT_10009e90f;
  local_75 = DAT_10009e91d + DAT_10009e910;
  local_74 = DAT_10009e91e + DAT_10009e911;
  local_73 = DAT_10009e91f + DAT_10009e912;
  local_72 = DAT_10009e920 + DAT_10009e913;
  local_71 = DAT_10009e921 + DAT_10009e914;
  if ((DAT_100105fa0 == (code *)0x0) &&
     (DAT_100105fa0 = (code *)FUN_10009b6b4(0xa799dcbbd0e60293), DAT_100105fa0 == (code *)0x0)) {
    uVar22 = 0;
  }
  else {
    pcVar4 = DAT_100105fa0;
    uVar22 = 0;
    uVar8 = 0x4a41dddb;
    lVar27 = 9;
    puVar25 = &DAT_10009e922;
    puVar26 = &DAT_10009ea15;
    do {
      FUN_10009b994(puVar25,*puVar26,&local_7d,&local_2560);
      pcVar11 = (char *)(*pcVar4)(&local_2560);
      if ((pcVar11 != (char *)0x0) && (*pcVar11 != '\0')) {
        uVar22 = uVar8 ^ uVar22;
      }
      uVar8 = uVar8 + 1;
      puVar25 = puVar25 + 0x1b;
      lVar27 = lVar27 + -1;
      puVar26 = puVar26 + 1;
    } while (lVar27 != 0);
  }
  if (DAT_100105fa8 == (code *)0x0) {
    DAT_100105fa8 = (code *)FUN_10009b6b4(0xaebf30704bc9f2c8);
  }
  pcVar4 = DAT_100105fa8;
  if (DAT_100105fb0 == (code *)0x0) {
    DAT_100105fb0 = (code *)FUN_10009b6b4(0xcbaef128826635f9);
    local_4720 = (code *)((ulong)local_4720._4_4_ << 0x20);
  }
  else {
    local_4720 = (code *)((ulong)local_4720 & 0xffffffff00000000);
  }
  if (pcVar4 == (code *)0x0) {
    local_4720._4_4_ = (uint)((ulong)local_4720 >> 0x20);
    local_4720 = (code *)CONCAT44(local_4720._4_4_,1);
  }
  if (DAT_100105fb0 == (code *)0x0) {
    local_4720._4_4_ = (uint)((ulong)local_4720 >> 0x20);
    local_4720 = (code *)CONCAT44(local_4720._4_4_,1);
  }
  if ((int)local_4720 == 0) {
    local_46f0 = (*DAT_100105fb0)();
    local_4650 = (code *)((ulong)local_4650 & 0xffffffffffffff00);
    local_4728 = (code *)CONCAT44(local_4728._4_4_,0x1000);
    local_46d0 = pcVar4;
    iVar10 = (*pcVar4)(local_46f0,&local_4650,0x1000);
    if (0 < iVar10) {
      if ((byte)local_4650 == 0) {
        uVar14 = 0;
      }
      else {
        uVar23 = 0;
        bVar16 = (byte)local_4650;
        do {
          local_3560 = CONCAT71(local_3560._1_7_,bVar16) | 0x20;
          if (bVar16 - 0x41 < 0x1a) {
            bVar16 = (byte)local_3560;
          }
          *(byte *)((long)&local_2560 + uVar23) = bVar16;
          uVar14 = uVar23 + 1;
          bVar16 = *(byte *)((long)&local_4650 + uVar23 + 1);
          bVar6 = uVar23 < 0x1107;
          uVar23 = uVar14;
        } while (bVar16 != 0 && bVar6);
      }
      lVar27 = 0;
      *(undefined1 *)((long)&local_2560 + uVar14) = 0;
      do {
        FUN_10009b994(&DAT_10009ea1e + lVar27 * 0xf,(&DAT_10009eb59)[lVar27],&local_7d,&local_3560);
        pbVar3 = (byte *)((long)&local_3560 + 1);
        bVar16 = (byte)local_3560;
        while (bVar16 != 0) {
          if (bVar16 - 0x41 < 0x1a) {
            pbVar3[-1] = bVar16 | 0x20;
          }
          bVar16 = *pbVar3;
          pbVar3 = pbVar3 + 1;
        }
        lVar12 = FUN_10009ba08(&local_2560,&local_3560);
        if (lVar12 != 0) {
          uVar22 = (int)lVar27 + 0xe3056f9fU ^ uVar22;
          break;
        }
        lVar27 = lVar27 + 1;
      } while (lVar27 != 0x15);
    }
  }
  if (DAT_100105fb8 == (code *)0x0) {
    DAT_100105fb8 = (code *)FUN_10009b6b4(0xc46e75b412db32e4);
  }
  pcVar4 = DAT_100105fb8;
  if (DAT_100105fc0 == (code *)0x0) {
    DAT_100105fc0 = (code *)FUN_10009b6b4(0xe738b8b74674272c);
    local_4650 = (code *)((ulong)local_4650 & 0xffffffff00000000);
    if (pcVar4 == (code *)0x0) goto LAB_10008f8c4;
LAB_10008f7c8:
    if (DAT_100105fc0 != (code *)0x0) goto LAB_10008f7cc;
LAB_10008f8d0:
    local_4650 = (code *)CONCAT44(local_4650._4_4_,1);
  }
  else {
    local_4650 = (code *)((ulong)local_4650 & 0xffffffff00000000);
    if (DAT_100105fb8 != (code *)0x0) goto LAB_10008f7c8;
LAB_10008f8c4:
    local_4650 = (code *)CONCAT44(local_4650._4_4_,1);
    if (DAT_100105fc0 == (code *)0x0) goto LAB_10008f8d0;
LAB_10008f7cc:
    pcVar5 = DAT_100105fc0;
    if ((uint)local_4650 == 0) {
      uVar8 = (*pcVar4)();
      FUN_10009b994(&DAT_10009eb6e,5,&local_7d,&local_2560);
      FUN_10009b994(&DAT_10009eb7d,5,&local_7d,&local_2550);
      FUN_10009b994(&DAT_10009eb8c,0xb,&local_7d,&local_2540);
      FUN_10009b994(&DAT_10009eb9b,9,&local_7d,&local_2530);
      FUN_10009b994(&DAT_10009ebaa,9,&local_7d,&local_2520);
      FUN_10009b994(&DAT_10009ebb9,0xf,&local_7d,&local_2510);
      FUN_10009b994(&DAT_10009ebc8,10,&local_7d,&local_2500);
      FUN_10009b994(&DAT_10009ebd7,10,&local_7d,&local_24f0);
      FUN_10009b994(&DAT_10009ebe6,9,&local_7d,&local_24e0);
      FUN_10009b994(&DAT_10009ebf5,0xc,&local_7d,&local_24d0);
      FUN_10009b994(&DAT_10009ec04,5,&local_7d,&local_24c0);
      FUN_10009b994(&DAT_10009ec13,8,&local_7d,&local_24b0);
      FUN_10009b994(&DAT_10009ec22,7,&local_7d,&local_24a0);
      FUN_10009b994(&DAT_10009ec31,0xd,&local_7d,&local_2490);
      if (uVar8 != 0) {
        uVar28 = 0;
        do {
          local_3560 = CONCAT44(local_3560._4_4_,uVar28);
          lVar27 = (*pcVar5)(uVar28);
          if (lVar27 != 0) {
            lVar12 = FUN_10009ba08(lVar27,&local_2560);
            uVar18 = 0x31ea5a27;
            if (lVar12 == 0) {
              lVar12 = FUN_10009ba08(lVar27,&local_2550);
              if (lVar12 == 0) {
                lVar12 = FUN_10009ba08(lVar27,&local_2540);
                if (lVar12 == 0) {
                  lVar12 = FUN_10009ba08(lVar27,&local_2530);
                  if (lVar12 == 0) {
                    lVar12 = FUN_10009ba08(lVar27,&local_2520);
                    if (lVar12 == 0) {
                      lVar12 = FUN_10009ba08(lVar27,&local_2510);
                      if (lVar12 == 0) {
                        lVar12 = FUN_10009ba08(lVar27,&local_2500);
                        if (lVar12 == 0) {
                          lVar12 = FUN_10009ba08(lVar27,&local_24f0);
                          if (lVar12 == 0) {
                            lVar12 = FUN_10009ba08(lVar27,&local_24e0);
                            if (lVar12 == 0) {
                              lVar12 = FUN_10009ba08(lVar27,&local_24d0);
                              if (lVar12 == 0) {
                                lVar12 = FUN_10009ba08(lVar27,&local_24c0);
                                if (lVar12 == 0) {
                                  lVar12 = FUN_10009ba08(lVar27,&local_24b0);
                                  if (lVar12 == 0) {
                                    lVar12 = FUN_10009ba08(lVar27,&local_24a0);
                                    if (lVar12 == 0) {
                                      lVar27 = FUN_10009ba08(lVar27,&local_2490);
                                      if (lVar27 == 0) goto LAB_10008fa34;
                                      uVar18 = 0x31ea5a34;
                                    }
                                    else {
                                      uVar18 = 0x31ea5a33;
                                    }
                                  }
                                  else {
                                    uVar18 = 0x31ea5a32;
                                  }
                                }
                                else {
                                  uVar18 = 0x31ea5a31;
                                }
                              }
                              else {
                                uVar18 = 0x31ea5a30;
                              }
                            }
                            else {
                              uVar18 = 0x31ea5a2f;
                            }
                          }
                          else {
                            uVar18 = 0x31ea5a2e;
                          }
                        }
                        else {
                          uVar18 = 0x31ea5a2d;
                        }
                      }
                      else {
                        uVar18 = 0x31ea5a2c;
                      }
                    }
                    else {
                      uVar18 = 0x31ea5a2b;
                    }
                  }
                  else {
                    uVar18 = 0x31ea5a2a;
                  }
                }
                else {
                  uVar18 = 0x31ea5a29;
                }
              }
              else {
                uVar18 = 0x31ea5a28;
              }
            }
            uVar22 = uVar18 ^ uVar22;
            uVar28 = uVar8;
          }
LAB_10008fa34:
          uVar28 = uVar28 + 1;
        } while (uVar28 < uVar8);
      }
    }
  }
  if (DAT_100105fc8 == (code *)0x0) {
    DAT_100105fc8 = (code *)FUN_10009b6b4(0x67d1d2d0c70180ce);
  }
  pcVar4 = DAT_100105fc8;
  if (DAT_100105fd0 == (code *)0x0) {
    DAT_100105fd0 = (code *)FUN_10009b6b4(0x67e0100007eff26f);
  }
  local_4650 = (code *)CONCAT44(local_4650._4_4_,(uint)(pcVar4 != (code *)0x0));
  local_3560 = CONCAT44(local_3560._4_4_,(uint)(DAT_100105fd0 != (code *)0x0));
  if ((uint)(DAT_100105fd0 != (code *)0x0) + (uint)(pcVar4 != (code *)0x0) == 2) {
    (*DAT_100105fd0)(&local_2560);
    if (local_2560._4_4_ == 0) {
      local_2560 = (code *)((long)&MACH_HEADER.magic + 1);
    }
    lVar27 = (*pcVar4)();
    uVar8 = 0;
    local_46d0 = (code *)((ulong)local_46d0 & 0xffffffff00000000);
    do {
      local_46d0 = (code *)CONCAT44(local_46d0._4_4_,(uint)local_46d0 ^ uVar8);
      uVar8 = uVar8 + 1;
    } while (uVar8 != 0x304e);
    lVar12 = (*pcVar4)();
    uVar23 = (ulong)local_2560 & 0xffffffff;
    uVar14 = (ulong)local_2560 >> 0x20;
    lVar13 = (*pcVar4)((ulong)local_46d0 & 0xffffffff);
    uVar8 = 0;
    local_46d0 = (code *)((ulong)local_46d0 & 0xffffffff00000000);
    do {
      local_46d0 = (code *)CONCAT44(local_46d0._4_4_,(uint)local_46d0 ^ uVar8);
      uVar8 = uVar8 + 1;
    } while (uVar8 != 0x304e);
    uVar15 = 0;
    if (uVar14 != 0) {
      uVar15 = ((lVar12 - lVar27) * uVar23) / uVar14;
    }
    lVar27 = (*pcVar4)();
    uVar23 = (ulong)local_2560 & 0xffffffff;
    uVar14 = (ulong)local_2560 >> 0x20;
    lVar12 = (*pcVar4)((ulong)local_46d0 & 0xffffffff);
    uVar8 = 0;
    local_46d0 = (code *)((ulong)local_46d0 & 0xffffffff00000000);
    do {
      local_46d0 = (code *)CONCAT44(local_46d0._4_4_,(uint)local_46d0 ^ uVar8);
      uVar8 = uVar8 + 1;
    } while (uVar8 != 0x304e);
    uVar19 = 0;
    if (uVar14 != 0) {
      uVar19 = ((lVar27 - lVar13) * uVar23) / uVar14;
    }
    if (uVar15 <= uVar19) {
      uVar19 = uVar15;
    }
    lVar27 = (*pcVar4)();
    uVar14 = 0;
    if ((ulong)local_2560 >> 0x20 != 0) {
      uVar14 = ((lVar27 - lVar12) * ((ulong)local_2560 & 0xffffffff)) / ((ulong)local_2560 >> 0x20);
    }
    if (uVar19 <= uVar14) {
      uVar14 = uVar19;
    }
    uVar8 = ((uint)uVar14 & 0xff) + 0x30b8a179;
    if (uVar14 < 0x464f094) {
      uVar8 = 0;
    }
    uVar22 = uVar8 ^ uVar22;
  }
  local_46d0 = (code *)CONCAT44(local_46d0._4_4_,0x71);
  local_4720 = (code *)CONCAT44(local_4720._4_4_,0x59);
  local_4728 = (code *)CONCAT44(local_4728._4_4_,0x48);
  local_46f0 = 0xffffffb9;
  local_46f4 = 0x79;
  local_46f8 = -0x6b;
  local_46fc = 0x46;
  local_4700 = -0x45;
  local_4704 = 0xd;
  local_4708 = 0x13;
  local_470c = 3;
  local_4710 = 8;
  if (DAT_100105fd8 == (code *)0x0) {
    DAT_100105fd8 = (code *)FUN_10009b6b4(0xa007fd1f6ae64e3a);
  }
  pcVar4 = DAT_100105fd8;
  if (DAT_100105fe0 == (code *)0x0) {
    DAT_100105fe0 = (code *)FUN_10009b6b4(0xab8f72d1c2fa9b6b);
  }
  local_4714 = (uint)(pcVar4 != (code *)0x0);
  local_4718 = (uint)(DAT_100105fe0 != (code *)0x0);
  if (local_4718 + local_4714 == 2) {
    local_4650 = (code *)(CONCAT44(local_46f8 + local_46f4,local_46f0 + (uint)local_4728) &
                         0xff000000ff);
    local_4648 = CONCAT44(local_4648._4_4_,local_4700 + local_46fc) & 0xffffffff000000ff;
    uVar9 = (*DAT_100105fe0)();
    local_4648 = CONCAT44(uVar9,(undefined4)local_4648);
    local_3560 = 0x288;
    _bzero(&local_2560,0x288);
    lVar27 = (*pcVar4)((int)local_4720 + (uint)local_46d0);
    if (((lVar27 == 0) && (0x3f < local_3560)) &&
       ((*(uint *)((long)&local_2560 + (long)local_4708 + (long)local_4704) >>
         (ulong)(local_4710 + local_470c & 0x1f) & 1) != 0)) {
      uVar22 = uVar22 ^ 0xd05a0d7a;
    }
  }
  uVar8 = uVar22;
  if ((DAT_100105fe8 != (code *)0x0) ||
     (DAT_100105fe8 = (code *)FUN_10009b6b4(0x67e0100007eff26f), DAT_100105fe8 != (code *)0x0)) {
    local_2560 = (code *)0x0;
    local_4650 = DAT_100105fe8;
    iVar10 = (*DAT_100105fe8)(&local_2560);
    if (iVar10 == 0) {
      uVar8 = uVar22 ^ 0xcadb22b6;
      if ((uint)local_2560 != 0 && local_2560._4_4_ != 0) {
        uVar8 = uVar22;
      }
    }
  }
  uVar22 = uVar8;
  if ((DAT_100105ff0 != (code *)0x0) ||
     (DAT_100105ff0 = (code *)FUN_10009b6b4(0xc47a400913d5acdb), DAT_100105ff0 != (code *)0x0)) {
    local_3560 = CONCAT44(local_3560._4_4_,0x13);
    local_46d0 = (code *)CONCAT44(local_46d0._4_4_,3);
    local_4720 = (code *)CONCAT44(local_4720._4_4_,0x16);
    local_2468 = 0;
    local_2470 = 0;
    local_2478 = 0;
    local_2480 = 0;
    local_2488 = 0;
    local_2490 = 0;
    local_2498 = 0;
    local_24a0 = 0;
    local_24a8 = 0;
    local_24b0 = 0;
    local_24b8 = 0;
    local_24c0 = 0;
    local_24c8 = 0;
    local_24d0 = 0;
    local_24d8 = 0;
    local_24e0 = 0;
    local_24e8 = 0;
    local_24f0 = 0;
    local_24f8 = 0;
    local_2500 = 0;
    local_2508 = 0;
    local_2510 = 0;
    local_2518 = 0;
    local_2520 = 0;
    local_2528 = 0;
    local_2530 = 0;
    local_2538 = 0;
    local_2540 = 0;
    local_2548 = 0;
    local_2550 = 0;
    local_2558 = 0;
    local_2560 = (code *)0x0;
    local_4728 = (code *)CONCAT44(local_4728._4_4_,0x40);
    local_4650 = DAT_100105ff0;
    iVar10 = (*DAT_100105ff0)(*(undefined4 *)PTR__mach_task_self__100102838,0x16,&local_2560,
                              &local_4728);
    if ((iVar10 == 0) &&
       ((7 < (uint)local_4728 &&
        (uVar22 = uVar8 ^ 0x723a8db9,
        (local_2560 != (code *)0x0 || local_2558 != 0) || (local_2550 != 0 || local_2548 != 0))))) {
      uVar22 = uVar8;
    }
  }
  if ((DAT_100105ff8 != (code *)0x0) ||
     (DAT_100105ff8 = (code *)FUN_10009b6b4(0x67d1d2d0c70180ce), DAT_100105ff8 != (code *)0x0)) {
    pcVar4 = DAT_100105ff8;
    local_4650 = (code *)((ulong)local_4650 & 0xffffffff00000000);
    local_2560 = DAT_100105ff8;
    uVar14 = (*DAT_100105ff8)();
    uVar8 = 0;
    do {
      local_4650 = (code *)CONCAT44(local_4650._4_4_,(uint)local_4650 ^ uVar8);
      uVar8 = uVar8 + 1;
    } while (uVar8 != 0x200);
    uVar23 = (*pcVar4)();
    uVar15 = (*pcVar4)();
    uVar8 = 0;
    do {
      local_4650 = (code *)CONCAT44(local_4650._4_4_,(uint)local_4650 ^ uVar8);
      uVar8 = uVar8 + 1;
    } while (uVar8 != 0x200);
    uVar19 = 0;
    if (uVar14 <= uVar23) {
      uVar19 = uVar23 - uVar14;
    }
    if (uVar14 > uVar23 || uVar23 - uVar14 == 0) {
      uVar19 = 0;
    }
    uVar14 = (*pcVar4)();
    uVar23 = (*pcVar4)();
    uVar8 = 0;
    do {
      local_4650 = (code *)CONCAT44(local_4650._4_4_,(uint)local_4650 ^ uVar8);
      uVar8 = uVar8 + 1;
    } while (uVar8 != 0x200);
    uVar21 = 0;
    if (uVar15 <= uVar14) {
      uVar21 = uVar14 - uVar15;
    }
    uVar1 = uVar19;
    if (uVar21 <= uVar19 - 1) {
      uVar1 = uVar21;
    }
    if (uVar14 <= uVar15) {
      uVar1 = uVar19;
    }
    uVar15 = (*pcVar4)();
    uVar14 = 0;
    if (uVar23 <= uVar15) {
      uVar14 = uVar15 - uVar23;
    }
    uVar19 = uVar1;
    if (uVar14 <= uVar1 - 1) {
      uVar19 = uVar14;
    }
    if (uVar15 <= uVar23) {
      uVar19 = uVar1;
    }
    local_3560 = CONCAT44(local_3560._4_4_,0x50bb9);
    local_46d0 = (code *)CONCAT44(local_46d0._4_4_,0xaf447);
    if (0xfffff < uVar19 - 1) {
      uVar22 = uVar22 ^ 0xe09cb84e;
    }
  }
  if (DAT_100106000 == (code *)0x0) {
    DAT_100106000 = (code *)FUN_10009b6b4(0x7e36c6db6c133704);
  }
  pcVar4 = DAT_100106000;
  if (DAT_100106008 == (code *)0x0) {
    DAT_100106008 = (code *)FUN_10009b6b4(0xaebf30704bc9f2c8);
  }
  pcVar5 = DAT_100106008;
  if ((pcVar4 != (code *)0x0) && (DAT_100106008 != (code *)0x0)) {
    local_46f0 = 1;
    local_4720 = pcVar4;
    iVar10 = (*pcVar4)(1,0,0,0);
    if ((iVar10 - 1U >> 2 < 0x937) &&
       ((uVar8 = (*pcVar4)(local_46f0,0,&local_2560,0x24dc), 0 < (int)uVar8 && (3 < uVar8)))) {
      uVar14 = 0;
      do {
        iVar10 = *(int *)((long)&local_2560 + uVar14 * 4);
        if (iVar10 < 1) {
          bVar6 = true;
        }
        else {
          local_3560 = local_3560 & 0xffffffffffffff00;
          local_46f4 = 0x1000;
          local_4728 = pcVar5;
          local_46f8 = iVar10;
          iVar10 = (*pcVar5)(iVar10,&local_3560,0x1000);
          if (iVar10 < 1) {
            bVar6 = true;
          }
          else {
            uVar23 = local_3560 & 0xff;
            if ((byte)local_3560 == '\0') {
              uVar15 = 0;
            }
            else {
              uVar19 = 0;
              do {
                cVar2 = (char)uVar23 + ' ';
                local_46fc = CONCAT31(local_46fc._1_3_,cVar2);
                cVar17 = (char)uVar23;
                if (((int)uVar23 - 0x41U & 0xff) < 0x1a) {
                  cVar17 = cVar2;
                }
                *(char *)((long)&local_4650 + uVar19) = cVar17;
                uVar15 = uVar19 + 1;
                bVar16 = *(byte *)((long)&local_3560 + uVar19 + 1);
                uVar23 = (ulong)bVar16;
              } while ((bVar16 != 0) && (uVar21 = uVar19 >> 1, uVar19 = uVar15, uVar21 < 0x875));
            }
            *(undefined1 *)((long)&local_4650 + uVar15) = 0;
            FUN_10009b994(&DAT_10009ec40,0xb,&local_7d,&local_46d0);
            lVar27 = FUN_10009ba08(&local_4650,&local_46d0);
            uVar28 = 0x60d7ba3;
            if (lVar27 == 0) {
              FUN_10009b994(&DAT_10009ec4b,10,&local_7d,&local_46d0);
              lVar27 = FUN_10009ba08(&local_4650,&local_46d0);
              if (lVar27 == 0) {
                FUN_10009b994(&DAT_10009ec56,8,&local_7d,&local_46d0);
                lVar27 = FUN_10009ba08(&local_4650,&local_46d0);
                if (lVar27 == 0) {
                  FUN_10009b994(&DAT_10009ec61,0xb,&local_7d,&local_46d0);
                  lVar27 = FUN_10009ba08(&local_4650,&local_46d0);
                  if (lVar27 == 0) {
                    FUN_10009b994(&DAT_10009ec6c,9,&local_7d,&local_46d0);
                    lVar27 = FUN_10009ba08(&local_4650,&local_46d0);
                    if (lVar27 == 0) {
                      FUN_10009b994(&DAT_10009ec77,7,&local_7d,&local_46d0);
                      lVar27 = FUN_10009ba08(&local_4650,&local_46d0);
                      if (lVar27 == 0) {
                        bVar6 = true;
                        goto LAB_100090a0c;
                      }
                      uVar28 = 0x60d7ba8;
                    }
                    else {
                      uVar28 = 0x60d7ba7;
                    }
                  }
                  else {
                    uVar28 = 0x60d7ba6;
                  }
                }
                else {
                  uVar28 = 0x60d7ba5;
                }
              }
              else {
                uVar28 = 0x60d7ba4;
              }
            }
            bVar6 = false;
            uVar22 = uVar28 ^ uVar22;
          }
        }
LAB_100090a0c:
        uVar14 = uVar14 + 1;
      } while ((uVar14 < uVar8 >> 2) && (bVar6));
    }
  }
  if (DAT_100106010 == 0) {
    DAT_100106010 = FUN_10009b6b4(0x8588fa91562c70df);
    bVar6 = DAT_100106010 != 0;
  }
  else {
    bVar6 = true;
  }
  if (DAT_100106018 == 0) {
    DAT_100106018 = FUN_10009b6b4(0x5d58d88005ba4fb4);
    bVar7 = DAT_100106018 != 0;
  }
  else {
    bVar7 = true;
  }
  if (DAT_100106020 == 0) {
    DAT_100106020 = FUN_10009b6b4(0x8222986e83ad3c5b);
    local_2560 = (code *)CONCAT44(local_2560._4_4_,0xd91236c1);
    if ((!bVar6 && !bVar7) && (DAT_100106020 == 0)) goto LAB_10009030c;
  }
  else {
    local_2560 = (code *)CONCAT44(local_2560._4_4_,0xd91236c1);
  }
  uVar22 = (uint)local_2560 ^ uVar22;
LAB_10009030c:
  if (DAT_100106028 == (code *)0x0) {
    DAT_100106028 = (code *)FUN_10009b6b4(0x14af1bb638658d08);
  }
  pcVar4 = DAT_100106028;
  if (DAT_100106030 == (code *)0x0) {
    DAT_100106030 = (code *)FUN_10009b6b4(0xd636b93297927ff7);
  }
  pcVar5 = DAT_100106030;
  if (pcVar4 != (code *)0x0) {
    local_2560 = (code *)((ulong)local_2560 & 0xffffffff00000000);
    local_4650 = (code *)CONCAT44(local_4650._4_4_,0x5a5a5a5);
    local_3560 = CONCAT44(local_3560._4_4_,0x15a5a5a5);
    local_46d0 = (code *)CONCAT44(local_46d0._4_4_,0xe639cea9);
    iVar10 = (*pcVar4)(0,0,&local_2560,4);
    if (iVar10 == 0) {
      if ((((uint)local_3560 ^ (uint)local_4650) & (uint)local_2560) != 0) {
        uVar22 = (uint)local_46d0 ^ uVar22;
        if (pcVar5 != (code *)0x0) {
          local_4720 = (code *)CONCAT44(local_4720._4_4_,0x19);
          local_4728 = (code *)CONCAT44(local_4728._4_4_,0x59);
          local_46f0 = 0x45db22d7;
          local_24e8 = 0;
          local_24f0 = 0;
          local_24f8 = 0;
          local_2500 = 0;
          local_2508 = 0;
          local_2510 = 0;
          local_2518 = 0;
          local_2520 = 0;
          local_2528 = 0;
          local_2530 = 0;
          local_2538 = 0;
          local_2540 = 0;
          local_2548 = 0;
          local_2550 = 0;
          local_2558 = 0;
          local_2560 = (code *)0x0;
          local_45e0 = 0;
          uStack_45d8 = 0;
          local_45f0 = 0;
          uStack_45e8 = 0;
          local_4600 = 0;
          uStack_45f8 = 0;
          local_4610 = 0;
          uStack_4608 = 0;
          local_4620 = 0;
          uStack_4618 = 0;
          local_4630 = 0;
          uStack_4628 = 0;
          local_4640 = 0;
          uStack_4638 = 0;
          local_4650 = (code *)0x0;
          local_4648 = 0;
          local_34e8 = 0;
          local_34f0 = 0;
          local_34f8 = 0;
          local_3500 = 0;
          local_3508 = 0;
          local_3510 = 0;
          local_3518 = 0;
          local_3520 = 0;
          local_3528 = 0;
          local_3530 = 0;
          local_3538 = 0;
          local_3540 = 0;
          local_3548 = 0;
          local_3550 = 0;
          local_3558 = 0;
          local_3560 = 0;
          local_4660 = 0;
          uStack_4658 = 0;
          local_4670 = 0;
          uStack_4668 = 0;
          local_4680 = 0;
          uStack_4678 = 0;
          local_4690 = 0;
          uStack_4688 = 0;
          local_46a0 = 0;
          uStack_4698 = 0;
          local_46b0 = 0;
          uStack_46a8 = 0;
          local_46c0 = 0;
          uStack_46b8 = 0;
          local_46d0 = (code *)0x0;
          uStack_46c8 = 0;
          local_46f4 = 0x20;
          iVar10 = (*pcVar5)(*(undefined4 *)PTR__mach_task_self__100102838,0x40,&local_2560,
                             &local_46f4,&local_4650,&local_3560,&local_46d0);
          if ((iVar10 == 0) && (local_46f4 != 0)) {
            uVar8 = local_46f4;
            if (0x1f < local_46f4) {
              uVar8 = 0x20;
            }
            uVar14 = (ulong)uVar8;
            piVar20 = (int *)&local_4650;
            puVar24 = (uint *)&local_2560;
            do {
              if (((*puVar24 & 0x40) != 0) && (*piVar20 != 0)) {
                uVar22 = local_46f0 ^ uVar22;
                break;
              }
              piVar20 = piVar20 + 1;
              uVar14 = uVar14 - 1;
              puVar24 = puVar24 + 1;
            } while (uVar14 != 0);
          }
        }
      }
    }
  }
  if (DAT_100106038 == (code *)0x0) {
    DAT_100106038 = (code *)FUN_10009b6b4(0x8d2f194295caa11f);
  }
  pcVar4 = DAT_100106038;
  if (DAT_100106040 == 0) {
    DAT_100106040 = FUN_10009b6b4(0x35d428ca588487de);
  }
  lVar27 = DAT_100106040;
  if (DAT_100106048 == 0) {
    DAT_100106048 = FUN_10009b6b4(0xaebf30704bc9f2c8);
  }
  lVar12 = DAT_100106048;
  if (DAT_100106050 == 0) {
    DAT_100106050 = FUN_10009b6b4(0xc47a400913d5acdb);
  }
  lVar13 = 0;
  local_3560 = CONCAT44(local_3560._4_4_,0x1aef8c);
  local_4650 = (code *)lVar27;
  local_4648 = lVar12;
  local_4640 = DAT_100106050;
  do {
    puVar24 = *(uint **)((long)&local_4650 + lVar13);
    if (puVar24 != (uint *)0x0) {
      if (pcVar4 != (code *)0x0) {
        local_2548 = 0;
        local_2550 = 0;
        local_2558 = 0;
        local_2560 = (code *)0x0;
        iVar10 = (*pcVar4)(puVar24,&local_2560);
        if (iVar10 == 0 || local_2558 == 0) {
          uVar22 = (uint)local_3560 ^ uVar22;
          break;
        }
      }
      local_2560 = (code *)CONCAT44(local_2560._4_4_,0xffe0001f);
      local_46d0 = (code *)CONCAT44(local_46d0._4_4_,0xd4200000);
      local_4720 = (code *)CONCAT44(local_4720._4_4_,0x58000050);
      local_4728 = (code *)CONCAT44(local_4728._4_4_,0xd61f0200);
      if (((*puVar24 & 0xffe0001f) == 0xd4200000) ||
         (((*puVar24 & 0xfffffffe) == 0x58000050 &&
          (((uint)*(byte *)((long)puVar24 + 5) << 8 | (byte)puVar24[1] & 0xffffffdf |
           (uint)*(byte *)((long)puVar24 + 6) << 0x10 | (uint)*(byte *)((long)puVar24 + 7) << 0x18)
           == 0xd61f0200)))) {
        uVar22 = (uint)local_3560 ^ uVar22;
        break;
      }
    }
    lVar13 = lVar13 + 8;
  } while (lVar13 != 0x18);
  if (*(long *)PTR____stack_chk_guard_100102830 == local_70) {
    return uVar22;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

