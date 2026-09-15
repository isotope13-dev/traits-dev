use strict;
use warnings;
use MIME::Base64;

# Documentation, not a call: system('/bin/sh', '-c', $command);
sub greeting {
    return decode_base64('SGVsbG8sIHdvcmxkIQ==');
}

1;
