var service = new ActiveXObject("Schedule.Service");
var task = service.NewTask(0);
task.RegistrationInfo.Author = "Example Developer";
service.GetFolder("root").RegisterTaskDefinition("MyTask", task, 6, null, null, 3);
