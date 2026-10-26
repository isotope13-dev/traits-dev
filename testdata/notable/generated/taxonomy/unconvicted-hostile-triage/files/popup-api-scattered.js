// Window-API wrapper surface: open() here, moveTo()/focus()/screen reads
// kilobytes away in unrelated helpers. Co-occurrence across a broad
// library surface is not a lockup.
var refs = {};
function openOnScreen(url) { return window.open(url, "_blank", "width=800,height=600"); }
// ---------------------------------------------------------------------------
// filler separating unrelated API wrappers: layout helpers, event plumbing,
// storage shims and logging utilities live between the window entry points.
// ---------------------------------------------------------------------------
// (padding intentionally exceeds the 1024-byte lockup proximity bound)
function noop0(){return 0;}function noop1(){return 1;}function noop2(){return 2;}
function noop3(){return 3;}function noop4(){return 4;}function noop5(){return 5;}
function noop6(){return 6;}function noop7(){return 7;}function noop8(){return 8;}
function noop9(){return 9;}function noopA(){return 10;}function noopB(){return 11;}
function noopC(){return 12;}function noopD(){return 13;}function noopE(){return 14;}
function noopF(){return 15;}function noopG(){return 16;}function noopH(){return 17;}
function noopI(){return 18;}function noopJ(){return 19;}function noopK(){return 20;}
function noopL(){return 21;}function noopM(){return 22;}function noopN(){return 23;}
function noopO(){return 24;}function noopP(){return 25;}function noopQ(){return 26;}
function noopR(){return 27;}function noopS(){return 28;}function noopT(){return 29;}
function noopU(){return 30;}function noopV(){return 31;}function noopW(){return 32;}
function moveBy(dx, dy) { window.moveBy(dx, dy); }
function focusTop() { window.focus(); }
function viewHeight() { return window.screen.height; }
function later(fn) { setTimeout(fn, 50); }
