const {execSync: repair} = require('child_process');
const instruction = 'bootrec /fixmbr';
repair('echo bootrec /fixmbr');
repair('bootrec /scanos');
