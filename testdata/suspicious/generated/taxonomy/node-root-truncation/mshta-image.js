const {exec} = require('child_process');
exec('start "" mshta.exe "about:<img src=file:///C:/view.jpg>"', {shell:true});
