const task = "Review the source code, explain the failing test, and suggest a patch. Do not modify files or cloud resources.";
exec(`q --trust-all-tools --no-interactive "${task}"`, () => {});
