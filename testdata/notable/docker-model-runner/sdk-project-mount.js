async function launch(client) {
 await client.docker.cli.exec('run', ['--volume', '/project:/work', 'lab.example/worker:2']);
 await client.extension.host.cli.exec('helper-tool', []);
}
