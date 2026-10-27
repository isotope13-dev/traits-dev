<?php
class Buffer {
    public function fetch() { return ''; }
    public function &fetchReference() { return $this->data; }
}
function &fetch($mode) { return $mode; }
