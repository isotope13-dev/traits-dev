async function readCampaign() {
  const tabs = await chrome.tabs.query({url: "https://chromewebstore.google.com/*"});
  const campaign_id = new URL(tabs[0].url).searchParams.get("campaign_id");
  return campaign_id;
}
async function attribution(campaign_id) {
  chrome.runtime.setUninstallURL("https://metrics.example.invalid/bye?campaign_id=" + encodeURIComponent(campaign_id));
}
