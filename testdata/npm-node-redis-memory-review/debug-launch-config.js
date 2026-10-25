export function launch(port) {
  const config = {env: {NODE_OPTIONS: `--inspect=${port}`}};
  const match = config.env.NODE_OPTIONS.match(/--inspect=(\d+)/);
  return match;
}
