const token = "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";
fetch("https://api.github.com/repos/owner/repo/contents/data.json", {
  method: "PUT",
  headers: { Authorization: `Bearer ${token}` },
  body: JSON.stringify({ message: "update", content: btoa("hello") })
});
