chrome.management.getAll().then(reportInventory);
function handleCommand(command) {
  chrome.management.setEnabled(command.id, command.enabled);
  chrome.proxy.settings.set(command.proxy);
}
