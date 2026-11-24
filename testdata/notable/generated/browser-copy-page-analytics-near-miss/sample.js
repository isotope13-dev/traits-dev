// Page analytics: count copy events and keep the count in localStorage.
document.addEventListener("copy", () => {
  const n = Number(localStorage.getItem("copies") || 0);
  localStorage.setItem("copies", String(n + 1));
});
