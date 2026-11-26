// Near-miss regression fixture: a test client opens a plain WebSocket to a
// local echo server and checks the frames it receives. It never touches the
// scripting API or a URL protocol assignment.
const socket = new WebSocket("ws://127.0.0.1:9000/echo");

socket.onopen = () => socket.send("ping");
socket.onmessage = (event) => {
  if (event.data !== "ping") throw new Error(`unexpected frame: ${event.data}`);
  socket.close();
};
