const {execSync: repair} = require('child_process');
repair('bootrec /fixmbr', {stdio: 'ignore'});
