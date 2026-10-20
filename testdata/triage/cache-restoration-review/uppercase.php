<?php
if (!FILE_EXISTS($cache)) {
    FILE_PUT_CONTENTS($cache, 'fresh data');
}
