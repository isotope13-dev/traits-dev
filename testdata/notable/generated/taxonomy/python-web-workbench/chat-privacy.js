const state = {incognito: false};
function togglePrivacy(on) { state.incognito = on; }
const button = `<button onclick="deleteFile('notes.txt')">Delete</button>`;
