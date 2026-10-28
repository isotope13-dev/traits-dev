const Kn = 'https://ads.publisher.invalid/open', Jn = 1, Yn = 90000, Qn = 'input, textarea, select, [contenteditable=""], [contenteditable="true"], .omnibox, .sidebar-omnibox, .newtab-search';
function St(_0x180530) {
    const _0x1c6cba = _0x180530;
    return !!(_0x1c6cba && 'closest' in _0x1c6cba && _0x1c6cba.closest(Qn));
}
function Xn() {
    let _0x3d22c3 = 0, _0x67f0ee = 0;
    const _0x38bbc5 = _0x280bb6 => {
        if (St(_0x280bb6.target) || St(document.activeElement))
            return;
        const _0x457b9a = Date.now();
        _0x457b9a - _0x67f0ee < Yn || (_0x3d22c3 += 1, !(_0x3d22c3 < Jn) && (_0x3d22c3 = 0, _0x67f0ee = _0x457b9a, window.open(Kn, '_blank', 'noopener,noreferrer')));
    };
    return document.addEventListener('click', _0x38bbc5, !0), () => document.removeEventListener('click', _0x38bbc5, !0);
}