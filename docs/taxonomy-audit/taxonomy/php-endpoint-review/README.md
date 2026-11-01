# PHP endpoint delivery review

The legacy `delivery/php-clicker` branch held three PE composites. A WebBrowser
class ID and PHP URL do not establish a clicker or even that the browser opens
that URL. WinInet, a mutex and a process-creation API do not establish a staged
loader. Both are now notable network-related PE profiles.

The WinInet, cached-download API, Run-key and registry-write combination is
retained as suspicious persistence evidence. Its description does not claim
that the downloaded file is the value written to the Run key.

The hostile hosts-file sinkhole rule selected the old dropper directory. Its
three corresponding alternatives now name the moved rules explicitly, so the
directory move alone does not discard those combinations.
