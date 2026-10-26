import { useState } from "react";

const tip = `You can also open Terminal, type cd, drag the folder into the terminal window, and press Enter. Then type pwd to see the full path.`;

export function PathHelp({ onPick }: { onPick: (path: string) => void }) {
  const [open, setOpen] = useState(false);
  return (
    <>
      <button type="button" onClick={() => setOpen(true)}>
        How to get a full path
      </button>
      {open ? (
        <div role="dialog">
          <p>{tip}</p>
          <p>Paste the absolute path into the input field.</p>
          <button type="button" onClick={() => onPick("/Users/you/project")}>
            Use example
          </button>
        </div>
      ) : null}
    </>
  );
}
