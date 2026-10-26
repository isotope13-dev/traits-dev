// Vetted data-store write dispatch: the command pattern every store,
// editor and CQRS handler uses. Dispatching a local write object is not
// remote tasking, so no C2 finding may fire here.
function execute(command) {
  const r = vet(command);
  if (r.refusal) return r.refusal;
  return store.execute(r.cmd);
}
