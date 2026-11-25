// Type tests for a chrome extension typings package.
declare const id: string;
chrome.management.uninstall(id); // $ExpectType Promise<void>
chrome.management.uninstall(id, { showConfirmDialog: true }); // $ExpectType Promise<void>
chrome.management.uninstall(id, () => {}); // $ExpectType void
chrome.management.uninstall(id, { showConfirmDialog: false }, () => {}); // $ExpectType void
chrome.management.uninstall(id, { showConfirmDialog: false }).then(() => {}); // $ExpectType Promise<void>
