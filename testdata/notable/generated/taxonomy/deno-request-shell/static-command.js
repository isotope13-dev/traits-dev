Deno.serve(async (req) => {
  const body = await req.text();
  await new Deno.Command("cmd", {args: ["/c", "echo ok"]}).output();
  return new Response(body);
});
