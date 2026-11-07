const html = `<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>`;
const listener = createCopilotNodeListener({runtime: new BuiltInAgent({}), cors: true});
server.listen(0, "127.0.0.1");
