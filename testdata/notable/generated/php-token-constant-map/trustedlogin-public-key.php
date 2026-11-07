<?php
namespace Acme\SupportIntegration;

use TrustedLogin\Client;
use TrustedLogin\Config;

$settings = array(
    'auth' => array(
        'api_key' => '1d9fc7a576cb88ed',
    ),
    'vendor' => array(
        'namespace'   => 'acme-events',
        'title'       => 'Acme Events',
        'support_url' => 'https://acme.example/support/',
    ),
);

$trusted_login = new Client(new Config($settings));
