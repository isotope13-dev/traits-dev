const listener = createCopilotNodeListener({runtime: new BuiltInAgent({}), cors: true});
server.listen(0, "127.0.0.1");
