// _malloc @ 10009e35c

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void * _malloc(size_t param_1)

{
  void *pvVar1;
  
                    /* WARNING: Could not recover jumptable at 0x00010009e364. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  pvVar1 = (void *)(*(code *)PTR__malloc_100104038)();
  return pvVar1;
}

