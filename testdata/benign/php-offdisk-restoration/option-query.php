<?php
$db = mysqli_connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME);
$result = mysqli_query($db, "SELECT option_value FROM {$table_prefix}options WHERE option_name = 'siteurl'");
$row = mysqli_fetch_assoc($result);
echo htmlspecialchars($row['option_value']);
