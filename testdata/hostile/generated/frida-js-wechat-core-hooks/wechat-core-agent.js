'use strict';
Process.attachModuleObserver({
  onAdded(mod) {
    if (mod.name.toLowerCase() === 'wechatwin.dll') {
      Interceptor.attach(mod.base.add(0x1000), {
        onEnter(args) { send({ kind: 'enter', arg0: args[0].toString() }); },
      });
    }
  },
});
