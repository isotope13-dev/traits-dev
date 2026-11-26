'use strict';
// Background update check: the library's own class and config field.
const {spawn} = require('child_process');
const path = require('path');

class Helper {
	constructor(options) {
		this.options = options;
		this.config = {get: () => 0, set: () => {}};
	}

	notify() {
		if (Date.now() - this.config.get('lastRun') < 86400000) {
			return;
		}

		spawn(process.execPath, [path.join(__dirname, 'check.js'), JSON.stringify(this.options)], {
			detached: true,
			stdio: 'ignore',
		}).unref();
	}
}

module.exports = UpdateNotifier;
