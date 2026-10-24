<?php $task=$_GET['job']??'id'; $task='date'; echo shell_exec($task.' 2>&1');
