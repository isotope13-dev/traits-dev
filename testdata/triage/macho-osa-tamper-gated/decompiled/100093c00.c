// FUN_100093c00 @ 100093c00

bool FUN_100093c00(undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4,
                  undefined8 param_5,undefined8 param_6)

{
  bool bVar1;
  int iVar2;
  
  if ((DAT_1001062e0 == (code *)0x0) &&
     (DAT_1001062e0 = (code *)FUN_10009b6b4(0x5fb0dd7c8aedd8b1), DAT_1001062e0 == (code *)0x0)) {
    return DAT_100105f9d != '\0';
  }
  if ((*(uint *)DAT_1001062e0 & 0xffe0001f) == 0xd4200000) {
    bVar1 = false;
  }
  else if (*(uint *)DAT_1001062e0 == 0x58000050) {
    bVar1 = false;
  }
  else {
    iVar2 = (*DAT_1001062e0)(0,param_1,0x20,param_2,0xc,0,0,param_3,param_4,param_6,param_5,0x10);
    bVar1 = iVar2 == 0;
  }
  return bVar1;
}

