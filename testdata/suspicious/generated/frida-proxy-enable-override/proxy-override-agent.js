'use strict';
// Hook the registry read that WinINet uses for proxy state and report it as disabled.
const advapi = Process.getModuleByName('advapi32.dll');
const read = advapi.getExportByName('RegQueryValueExW');
Interceptor.attach(read, {
  onEnter(args) { this.name = args[1].isNull() ? '' : args[1].readUtf16String(); this.data = args[4]; },
  onLeave(ret) {
    if (this.name === 'ProxyEnable' && ret.toInt32() === 0 && !this.data.isNull()) this.data.writeU32(0);
  }
});
