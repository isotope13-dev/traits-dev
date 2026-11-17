const flag = process.env.FLAG;
function formatFlag() {
  return `https://collector.example.invalid/submit?flag=${encodeURIComponent(flag)}`;
}
formatFlag();
