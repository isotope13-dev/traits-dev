import {execFileSync} from 'child_process';
execFileSync('npm', ['view', 'example', 'version']);
