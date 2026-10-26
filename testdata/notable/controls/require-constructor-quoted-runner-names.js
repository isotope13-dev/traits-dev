// Counts and names in documentation do not establish a shared evaluator.
const example = `
function runOne() {}
function runTwo() {}
function runThree() {}
function execOne() {}
function execTwo() {}
function execThree() {}
`;
function compileModule(moduleText) {
  return new Function("require", "module", moduleText);
}
