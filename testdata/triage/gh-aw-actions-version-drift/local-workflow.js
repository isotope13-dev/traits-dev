// A compiler test runs its generated workflow against injected service doubles.
const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor;
export async function checkWorkflow(script, localRequire, core, github, context) {
  await new AsyncFunction("require", "core", "github", "context", script)(
    localRequire, core, github, context
  );
}
