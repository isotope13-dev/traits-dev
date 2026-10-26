const session = await vscode.authentication.getSession('github', ['repo'], {createIfNone: false, silent: true});
const token = session?.accessToken;
