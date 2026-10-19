// _pthread_once @ 10009e374

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int _pthread_once(pthread_once_t *param_1,void *param_2)

{
  int iVar1;
  
                    /* WARNING: Could not recover jumptable at 0x00010009e37c. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  iVar1 = (*(code *)PTR__pthread_once_100104048)((int)param_1);
  return iVar1;
}

