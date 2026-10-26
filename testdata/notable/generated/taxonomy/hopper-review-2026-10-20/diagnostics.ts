import { GuardRpc } from "../opencode-shell-guard/rpc.js";
export async function digest(ctx: any) { const guard = await ctx.rpc(GuardRpc).recent({ limit: 50 }); const latestBlock = guard.blocks.at(-1); return {guardLatestCommand: latestBlock?.command ?? ""}; }
