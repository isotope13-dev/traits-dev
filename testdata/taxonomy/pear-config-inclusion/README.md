PEAR configuration injection regression fixtures inspired by Exploit-DB 52690.

The Python and JavaScript fixtures include PEAR through double-encoded parent paths, write PHP file-read code through CGI config-create arguments, then include the generated file. Both should match pear-config-create-php-injection and pear-traversal-php-injection-chain. The benign fixtures contain ordinary config-create arguments or unrelated PHP text and must match neither hostile rule.

Indicator handling: pearcmd.php and wp-pear-rce-flag.php are file basenames, not hostnames. x.com links to reporting; the loopback target is a lab address. No malicious endpoint or article-supplied SHA256 is present. PURLS records the demonstrated WordPress release and Docker tag. The article additionally describes an affected range from 4.7 through 7.0.2, rather than identifying each release individually.
