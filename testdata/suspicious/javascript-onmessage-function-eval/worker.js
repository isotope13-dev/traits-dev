const worker = new Worker('./task.js');

worker.onmessage = function (e) {
  eval(e.data.code);
};

worker.postMessage({ ready: true });
