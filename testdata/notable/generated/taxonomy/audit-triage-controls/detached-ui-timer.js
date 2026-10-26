const {spawn} = require('child_process');
setTimeout(() => renderPanel(), 120000);
function launchTool(file) { spawn(file, [], {detached:true}); }
