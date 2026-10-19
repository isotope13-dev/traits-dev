// FUN_10009d6dc @ 10009d6dc

void FUN_10009d6dc(void)

{
  long lVar1;
  
  lVar1 = 0;
  do {
    *(uint *)((long)&DAT_1001060e8 + lVar1) =
         *(uint *)((long)&DAT_10009eef8 + lVar1) ^ *(uint *)((long)&DAT_10009edf8 + lVar1) ^
         *(uint *)((long)&DAT_10009ecf8 + lVar1);
    lVar1 = lVar1 + 4;
  } while (lVar1 != 0x100);
  return;
}

