<?php
(new Users())->createUser(['name' => $name, 'email' => $email]);
$userModel->createUser(['name' => 'Admin', 'password' => $hash]);
// IAM uses createUser(['UserName' => $name]); this comment is documentation.
$source = '$iam->createUser(["UserName" => $name])';
