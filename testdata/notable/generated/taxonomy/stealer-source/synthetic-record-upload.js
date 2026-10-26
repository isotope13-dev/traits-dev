function recordCanvas(canvas) {
    const stream = canvas.captureStream();
    const recorder = new MediaRecorder(stream);
    recorder.ondataavailable = (event) => {
        const recording = event.data;
        const form = new FormData();
        form.append("recording", recording, "animation.webm");
        fetch("https://capture.invalid/recording", {method: "POST", body: form});
    };
    recorder.start();
}
