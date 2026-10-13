trait ToolHook { fn before_exec(&self); }
fn unrelated() { let message = "pre_exec("; }
