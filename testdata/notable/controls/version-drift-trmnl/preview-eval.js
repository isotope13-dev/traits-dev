function fetchPreview() { fetch("/preview").then(async response => { const js = await response.text(); eval(js); }); }
