// Type tests for a chrome extension typings package (never executed).
declare const id: string;
chrome.management.uninstall(id); 
chrome.management.uninstall(id, { showConfirmDialog: true }); 
chrome.management.uninstall(id, () => {}); 
chrome.management.uninstall(id, { showConfirmDialog: false }, () => {}); 
// @ts-expect-error
chrome.management.uninstall(); 
