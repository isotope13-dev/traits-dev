<?php
// Field-to-constant map: the value names a configuration constant whose
// value is supplied by the deployment, it is not a secret itself.
function constant_fields() {
    return array(
        'api_key'    => 'ACME_STORAGE_API_KEY',
        'secret_key' => 'ACME_STORAGE_SECRET_KEY',
    );
}
