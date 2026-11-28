// A native lifecycle event and a real browser edit listener may coexist.
_reactNative.AppState.addEventListener('change', state => save(state));
input.addEventListener('change', event => update(event.target.value));
