<?php
function instrumentSource($source, $prefix)
{
    return str_replace('function inspect()', $prefix.'function inspect()', $source);
}
