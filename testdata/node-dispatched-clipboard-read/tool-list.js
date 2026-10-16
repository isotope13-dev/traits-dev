// Tool inventory for documentation: a bare list and prose mention neither
// dispatch a helper nor pass it as a command.
// Use pbpaste | pbcopy on macOS.
const tools = ['pbpaste', 'pbcopy'];
export function toolCount() {
  return tools.length;
}
