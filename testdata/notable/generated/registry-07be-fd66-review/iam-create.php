<?php
$iam->createUser(['UserName' => 'new-user']);
$client->createUser(['Path' => '/', 'UserName' => $name]);
(new \Aws\Iam\IamClient($config))->createUser(['UserName' => $name]);
