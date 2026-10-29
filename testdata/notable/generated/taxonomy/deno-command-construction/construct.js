Deno.serve(req => new Response("/exec"));
const task = new Deno.Command("cmd", { args: ["/c", "echo safe"] });
