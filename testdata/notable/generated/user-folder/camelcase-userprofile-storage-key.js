function load(cb) {
  chrome.storage.local.get(["userProfile", "subscription"], (e) => {
    const userProfile = e.userProfile;
    cb(userProfile, e.subscription);
  });
}
