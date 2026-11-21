chrome.storage.local.get(["loginData"], (state) => {
  const savedPass = state.loginData.pass;
  document.querySelector("#password").value = savedPass;
});
