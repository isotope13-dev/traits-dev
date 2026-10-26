// Dialog centering helpers (cf. MavensMate mavensmate.js): subtracting half
// the dialog size from the screen size centers the window on it. The
// subtrahend only resembles an off-desktop coordinate; it parks nothing.
function resizeAndCenterWindowSpecific(width, height) {
    window.resizeTo(width, height + 160);
    window.moveTo((screen.width-width)/2,(screen.height-document.getElementById('wrapper').offsetHeight-(width+15))/2);
}

function centerWindow() {
    window.moveTo((screen.width-385)/2,(screen.height-240)/2-190);
}
//window.moveTo((screen.width-385)/2,(screen.height-document.getElementById('wrapper').offsetHeight-400)/2);
