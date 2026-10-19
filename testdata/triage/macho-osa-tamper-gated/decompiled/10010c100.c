// _abort @ 10010c100

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void _abort(void)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}

