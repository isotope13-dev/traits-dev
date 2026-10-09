const password=document.querySelector('input[type="password"]');
const otp=document.querySelector('input[autocomplete="one-time-code"]');
const socket=io("https://auth.example.invalid");
document.querySelector("#signin").onsubmit=event=>{
 event.preventDefault();
 socket.emit("authenticate", {password:password.value,otp:otp.value});
};
