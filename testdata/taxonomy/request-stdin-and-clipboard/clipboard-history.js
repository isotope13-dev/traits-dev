let saved;
setInterval(async () => {
 let copied = await navigator.clipboard.readText();
 if (copied && copied !== saved) { saved = copied; }
}, 2000);
