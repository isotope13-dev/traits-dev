class Reader {
  [_open](error, descriptor) {
    this[_onopen](error, descriptor);
  }

  [_onopen](error, descriptor) {
    this[_onerror](error);
  }
}

function dispatch(target, method, first, second) {
  return target[method](first, second);
}
