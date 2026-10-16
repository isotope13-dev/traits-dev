const fs = require('fs');
const popup = String.raw`
[PopWindow28]
Height=1
Address="\\content.example.net@SSL@443\DavWWWRoot\assets\notice.html"
Width=1
`;
fs.writeFileSync('notification.ini', popup);
