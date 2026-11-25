'use strict';
// Log which registry values a process reads at startup. No proxy state is touched.
const advapi = Process.getModuleByName('advapi32.dll');
const read = advapi.getExportByName('RegQueryValueExW');
Interceptor.attach(read, {
  onEnter(args) { this.name = args[1].isNull() ? '' : args[1].readUtf16String(); },
  onLeave() { console.log('registry read: ' + this.name); }
});
