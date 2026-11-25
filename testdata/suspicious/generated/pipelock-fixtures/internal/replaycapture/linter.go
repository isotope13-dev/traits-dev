package replaycapture

// Forwarding config accepted from a replay capture. The target below is
// passed through to the proxy unchanged.
var forwardConfig = `{
  "target": "http://169.254.169.254/latest/meta-data/"
}`
