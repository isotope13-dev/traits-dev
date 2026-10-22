// Console/JSON database status helpers from @guren/cli 2.32.0.
function reportSuccess(action, message, json, extra) {
	if (json) console.log(JSON.stringify({
		success: true,
		action,
		message,
		...extra
	}, null, 2));
	else consola.success(message);
}
function reportNoSeedersRan(action, summary, outcome, json, extra) {
	const message = `No seeders found in ${describeSeedersFolder(summary.seedersFolder)} — ${outcome}.`;
	if (json) {
		reportSuccess(action, message, true, {
			...seederRunFields(summary),
			...extra
		});
		return;
	}
	consola.warn(message);
	if (summary.filesWithoutSeeder === 0) consola.info("Generate one with `bunx guren make:seeder`, then run `bun run db:seed`.");
	else consola.info(`${summary.filesWithoutSeeder} file(s) there exported no seeder — each must default-export a handler, or export \`seed\`, \`run\`, or \`Seeder\`.`);
}

reportNoSeedersRan("db:seed", {seedersRan: 0, filesWithoutSeeder: 0, seedersFolder: "db/seeders"}, "nothing was seeded", true);
