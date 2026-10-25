const tools = { child_process: require('child_process') };
function run(program, args) {
  return tools['child_process']['spawn'](program, args);
}
