'use strict';
const open = Module.getExportByName(null, 'open');
Interceptor.attach(open, {
  onEnter(args) { send({ kind: 'open', path: args[0].readUtf8String() }); },
});
