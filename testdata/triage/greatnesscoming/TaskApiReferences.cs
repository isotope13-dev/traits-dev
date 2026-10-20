// Compile-only control: enum declarations and interface references register no tasks.
public enum TaskLogon { TASK_LOGON_SERVICE_ACCOUNT = 5 }
public enum TaskRunLevel { TASK_RUNLEVEL_HIGHEST = 1 }
public enum TaskTrigger { TASK_TRIGGER_BOOT = 8, TASK_TRIGGER_LOGON = 9 }
public interface ITaskService {
    object RegisterTaskDefinition(string name);
    void CreateServiceTask();
}
