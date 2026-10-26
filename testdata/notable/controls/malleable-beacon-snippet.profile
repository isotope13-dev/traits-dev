set sleeptime "78126";
set jitter "20";
set dns_idle "0.0.0.0";
set maxdns "255";

http-get {
    set uri "/search";
    client {
        parameter "search" "W1hfIG49ZmluZF9jaGlsZHJlbg==";
        metadata {
            base64url;
            parameter "q";
        }
    }
}
