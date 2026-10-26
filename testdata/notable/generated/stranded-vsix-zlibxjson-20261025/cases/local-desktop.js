const screenshot = require('screenshot-desktop');
const { mouse, Button, Point } = require('@nut-tree-fork/nut-js');
async function inspect() { const frame = await screenshot(); await mouse.click(Button.LEFT); }
