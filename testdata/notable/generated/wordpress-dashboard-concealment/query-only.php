<?php
$users = get_users(['login__not_in' => ['disabled']]);
