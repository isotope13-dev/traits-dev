// Parameterized keyword-table writes: browser-profile tooling that inserts
// provider rows through bound statements shares the INSERT primitive
// without carrying the {searchTerms} template inside the statement.
const insert = db.prepare(
  "insert into keywords ( short_name, keyword, favicon_url, url ) values ( ?, ?, ?, ? )"
);
for (const engine of engines) {
  insert.run(engine.name, engine.keyword, engine.icon, engine.url);
}
