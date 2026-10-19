// _task_info @ 10009e38c

/* WARNING: Unknown calling convention -- yet parameter storage is locked */

kern_return_t
_task_info(task_name_t target_task,task_flavor_t flavor,task_info_t task_info_out,
          mach_msg_type_number_t *task_info_outCnt)

{
  kern_return_t kVar1;
  
                    /* WARNING: Could not recover jumptable at 0x00010009e394. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  kVar1 = (*(code *)PTR__task_info_100104058)(target_task,flavor);
  return kVar1;
}

