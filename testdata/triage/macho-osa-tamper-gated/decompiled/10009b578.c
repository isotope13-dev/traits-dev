// entry @ 10009b578

/* WARNING: Removing unreachable block (ram,0x00010009b5e4) */

undefined8 entry(uint param_1)

{
  uint uVar1;
  
  uVar1 = 0;
  if ((&PTR__snprintf_100101ee8)[param_1 % 0x37] != (undefined *)0x1 || (int)param_1 < 0xf4241) {
    uVar1 = param_1 % 0xf2;
  }
  (*(code *)(&PTR_LAB_100101758)[uVar1])(0xab84630a,0x517e8755);
  return 0;
}

