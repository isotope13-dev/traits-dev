# Authenticated remote administration uses this same disposable task lifecycle.
binding = r'ncacn_np:%s[\pipe\atsvc]'
tsch.hSchRpcRegisterTask(dce, task, xml)
tsch.hSchRpcRun(dce, task)
tsch.hSchRpcGetLastRunInfo(dce, task)
tsch.hSchRpcDelete(dce, task)
