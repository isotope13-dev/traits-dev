declare module 'node:child_process' {
  interface SpawnOptions { detached?: boolean; }
  function spawn(command: string, options?: SpawnOptions): ChildProcess;
}
