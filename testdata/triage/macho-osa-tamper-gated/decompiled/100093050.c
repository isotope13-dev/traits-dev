// FUN_100093050 @ 100093050

void FUN_100093050(undefined8 *param_1)

{
  code *pcVar1;
  code *pcVar2;
  undefined8 uVar3;
  long lVar4;
  undefined1 local_4f;
  undefined1 local_4e;
  undefined1 local_4d;
  undefined1 local_4c;
  undefined1 local_4b;
  undefined1 local_4a;
  undefined1 local_49;
  undefined1 local_48;
  undefined1 local_47;
  undefined1 local_46;
  undefined1 local_45;
  undefined1 local_44;
  undefined1 local_43;
  undefined1 local_42;
  undefined1 local_41;
  undefined1 local_40;
  undefined1 local_3f;
  undefined1 local_3e;
  undefined1 local_3d;
  undefined1 local_3c;
  undefined1 local_3b;
  undefined1 local_3a;
  undefined1 local_39;
  long local_38;
  
  local_38 = 0;
  if (DAT_100106230 == (code *)0x0) {
    DAT_100106230 = (code *)FUN_10009b6b4(0x33f2e954be3026ce);
  }
  pcVar1 = DAT_100106230;
  if (DAT_100106238 == (code *)0x0) {
    DAT_100106238 = (code *)FUN_10009b6b4(0x47c2a1606c55747e);
  }
  pcVar2 = DAT_100106238;
  if (pcVar1 == (code *)0x0 || DAT_100106238 == (code *)0x0) {
    param_1[2] = 0;
    param_1[3] = 0;
    *param_1 = 0;
    param_1[1] = 0;
  }
  else {
    local_40 = 0;
    local_41 = 0x20;
    local_42 = 0xc1;
    local_43 = 0xeb;
    local_44 = 0x51;
    local_45 = 0x7c;
    local_46 = 0xd5;
    local_47 = 0x11;
    local_48 = 0xfe;
    local_3f = 0x5f;
    local_3e = 0x5f;
    local_3d = 0x54;
    local_3c = 0x45;
    local_3b = 0x58;
    local_3a = 0x54;
    local_39 = 0;
    local_4f = 0x5f;
    local_4e = 0x5f;
    local_4d = 0x74;
    local_4c = 0x65;
    local_4b = 0x78;
    local_4a = 0x74;
    local_49 = 0;
    uVar3 = (*pcVar1)(0);
    lVar4 = (*pcVar2)(uVar3,&local_3f,&local_4f,&local_38);
    local_3f = 0;
    local_3e = 0;
    local_3d = 0;
    local_3c = 0;
    local_3b = 0;
    local_3a = 0;
    local_39 = 0;
    local_4f = 0;
    local_4e = 0;
    local_4d = 0;
    local_4c = 0;
    local_4b = 0;
    local_4a = 0;
    local_49 = 0;
    if ((lVar4 == 0) || (local_38 == 0)) {
      param_1[2] = 0;
      param_1[3] = 0;
      *param_1 = 0;
      param_1[1] = 0;
    }
    else {
      FUN_10009cde8(lVar4,local_38,param_1);
    }
  }
  return;
}

