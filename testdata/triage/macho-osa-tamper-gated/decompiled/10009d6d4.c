// FUN_10009d6d4 @ 10009d6d4

uint FUN_10009d6d4(uint param_1,uint param_2)

{
  return param_1 >> (param_2 & 0x1f) | param_1 << 0x20 - (param_2 & 0x1f);
}

