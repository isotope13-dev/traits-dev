<?php $key='example'; $x=base64_decode($_POST['data']); $c=''; for($i=0;$i<strlen($x);$i++) { $c .= chr(ord($x[$i]) ^ ord($key[$i % strlen($key)])); } echo htmlspecialchars($c);
