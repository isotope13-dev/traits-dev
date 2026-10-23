<?php
// /e is a legacy callback mechanism. The second call does not evaluate PHP.
preg_replace('/([a-z]+)/e', 'strtoupper("$1")', $content);
preg_replace('/name/', $_POST['label'], $content);
