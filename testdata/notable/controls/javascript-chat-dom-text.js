function renderChat(content) {
  const bubble = document.createElement('div');
  bubble.textContent = content;
  document.body.appendChild(bubble);
}

// Creating an unrelated script must not classify the div body as executable.
const helper = document.createElement('script');
helper.src = '/highlight.js';
document.head.appendChild(helper);
