let text = '';
for (let i = 0; i < 1000000; i++) {
  text = text + i.toString();
  history.pushState({}, '', text);
}
