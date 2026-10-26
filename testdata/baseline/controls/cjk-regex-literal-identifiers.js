// ASCII identifiers checked against CJK regular expressions: the non-ASCII
// bytes are pattern content, not the declared names.
function checkText(input) {
  return /(?:高风险|严重问题)/.test(input);
}
const bottleneckPattern = /(?:性能)?瓶颈/;
let hitCount = 0;
